from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
JWT_SECRET_KEY = "secret_key_Paterno"

#Funzione per inizializzare il database e creare la tabella utenti se non esiste
def init_db():
    with sqlite3.connect("utenti.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()


#Funzione per generare un token JWT
def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "username": username,
        "exp": expiration_time
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return token


#Funzione per verificare il token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        return None  #Token scaduto
    except jwt.InvalidTokenError:
        return None  #Token non valido


#Rotta per il login
@app.route("/", methods=["GET", "POST"])
def login():
    nomeC = request.cookies.get("mycookie")  #Controllo se esiste un cookie salvato
    if nomeC:
        #Verifico il token nel cookie
        verified_username = verify_token(nomeC)
        if verified_username:
            #Se il token è valido, reindirizzo alla home
            return redirect(url_for("home", username=verified_username))
        else:
            #Se il token non è valido, elimino il cookie e proseguo con il login
            risposta = make_response(redirect(url_for("login")))
            risposta.delete_cookie("mycookie")  #Elimino il cookie
            return risposta

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #Controllo le credenziali nel database
        with sqlite3.connect("utenti.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM utenti WHERE username = ?", (username,))
            user = cursor.fetchone()

        if user is not None:
            if check_password_hash(user[0], password):  #Verifico l'hash della password
                #Genero il token JWT
                token = generate_token(username)

                #Imposto il cookie con il token
                risposta = make_response(redirect(url_for("home", username=username)))
                risposta.set_cookie("mycookie", token, max_age=60*60*24)  #Imposta il cookie
                return risposta
        else:
            return render_template("login.html", alert="Utente non trovato")

    return render_template('login.html')


#Rotta per la creazione di un nuovo account
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            #Inserisco il nuovo utente nel database
            with sqlite3.connect("utenti.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO utenti (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("create_account.html", alert="Utente già esistente")

    return render_template('create_account.html')


#Rotta per la homepage
@app.route("/home/<username>", methods=["GET"])
def home(username):
    #Verifico se il token nel cookie è valido
    token = request.cookies.get("mycookie")
    if token:
        verified_username = verify_token(token)
        if verified_username:
            return render_template('home.html', username=verified_username)

    #Se il token non è valido, elimino il cookie e reindirizzo al login
    risposta = make_response(redirect(url_for("login")))
    risposta.delete_cookie("mycookie")  #Elimino il cookie
    return risposta


#Rotta per il logout
@app.route("/logout")
def logout():
    risposta = make_response(redirect(url_for("login")))
    risposta.delete_cookie("mycookie")  #Elimino il cookie
    return risposta


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=4444)
