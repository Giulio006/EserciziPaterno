from pynput import keyboard

# Quando premo
def on_press(key):
    if hasattr(key, 'char') and key.char is not None: # Controllo che il tasto premuto sia una lettera
        print(f"Tasto premuto: {key.char}")

# Quando rilascio
def on_release(key):
    if key == keyboard.Key.esc:     # Se premo ESC si interrompe
        return False

# Avvio l'ascolto dei tasti
def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()