from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

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

#Rotta per la pagina iniziale
@app.route("/")
def index():
    nomeC = request.cookies.get("mycookie")  #Controllo se esiste un cookie salvato
    if nomeC:
        return redirect(url_for("home", username=nomeC))  #Se il cookie esiste, reindirizzo alla home
    return redirect(url_for("login"))  #Se il cookie non esiste, reindirizzo al login

#Rotta per il login
@app.route("/login", methods=["GET", "POST"])
def login():
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
                risposta = redirect(url_for("home", username=username))
                risposta.set_cookie("mycookie", username, max_age=60*60*24)  #Imposto il cookie
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
    return render_template('home.html', username=username)

#Rotta per il logout
@app.route("/logout")
def logout():
    session.pop("username", None)

    risposta = make_response(redirect(url_for("login")))
    risposta.delete_cookie("mycookie")  #Elimino il cookie
    return risposta

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=4444)
