import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QMessageBox, QInputDialog, QComboBox
import random

def load_words():
    try:
        with open("words.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_words(words):
    with open("words.json", "w") as file:
        json.dump(words, file, ensure_ascii=False, indent=4)

class WordLearningApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikacja do nauki słówek")
        self.setGeometry(100, 100, 400, 500)

        self.words = load_words()  

        self.layout = QVBoxLayout()
        
        self.language_select = QComboBox(self)
        self.language_select.addItems(["Wybierz język", "Angielski"])

        self.word_input = QLineEdit(self)
        self.word_input.setPlaceholderText("Wpisz słówko")
        self.translation_input = QLineEdit(self)
        self.translation_input.setPlaceholderText("Wpisz tłumaczenie")

        self.add_button = QPushButton("Dodaj słówko", self)
        self.word_list = QListWidget(self)
        self.quiz_button = QPushButton("Start quizu", self)

        # Dodanie elementów do layoutu
        self.layout.addWidget(QLabel("Wybierz język"))
        self.layout.addWidget(self.language_select)
        self.layout.addWidget(QLabel("Wpisz słówko"))
        self.layout.addWidget(self.word_input)
        self.layout.addWidget(QLabel("Wpisz tłumaczenie"))
        self.layout.addWidget(self.translation_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.word_list)
        self.layout.addWidget(self.quiz_button)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.add_word)
        self.quiz_button.clicked.connect(self.start_quiz)

        self.update_word_list()

    def add_word(self):
        language = self.language_select.currentText()
        word = self.word_input.text()
        translation = self.translation_input.text()

        if language == "Wybierz język":
            self.show_message("Błąd", "Proszę wybrać język.")
            return

        if word and translation:
            self.words.append({"language": language, "word": word, "translation": translation})
            save_words(self.words) 
            self.update_word_list()
            self.word_input.clear()
            self.translation_input.clear()
        else:
            self.show_message("Błąd", "Proszę wprowadzić zarówno słówko, jak i tłumaczenie.")

    def update_word_list(self):
        self.word_list.clear()
        for word in self.words:
            self.word_list.addItem(f"{word['language']} - {word['word']} -> {word['translation']}")

    def start_quiz(self):
        if not self.words:
            self.show_message("Brak słówek", "Brak dostępnych słówek do quizu. Proszę dodać słówka.")
            return

        language = self.language_select.currentText()

        if language == "Wybierz język":
            self.show_message("Błąd", "Proszę wybrać język do quizu.")
            return

        filtered_words = [word for word in self.words if word["language"] == language]

        if not filtered_words:
            self.show_message("Brak słówek", f"Brak słówek w języku {language} do quizu.")
            return

        random_word = random.choice(filtered_words)
        answer, ok = QInputDialog.getText(self, "Quiz", f"Jak przetłumaczyć słowo '{random_word['word']}'?")

        if ok and answer.strip().lower() == random_word['translation'].lower():
            self.show_message("Dobrze!", "Gratulacje! Odpowiedź poprawna.")
        else:
            self.show_message("Błąd", f"Niepoprawna odpowiedź. Prawidłowe tłumaczenie to: {random_word['translation']}")

    def show_message(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordLearningApp()
    window.show()
    sys.exit(app.exec())
