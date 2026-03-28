import random
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton
)
from UI.utils.editable_text import EditableText

class UnscrambleSection(QFrame):

    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent
        self.word_inputs = []

        self.init_ui()

    def init_ui(self):

        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        move_up = QPushButton("↑")
        move_down = QPushButton("↓")
        delete_button = QPushButton("Delete")

        move_up.clicked.connect(self.move_up)
        move_down.clicked.connect(self.move_down)
        delete_button.clicked.connect(self.delete_section)

        button_layout.addWidget(move_up)
        button_layout.addWidget(move_down)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        # Title
        self.title_input = EditableText(self.main_window, "Unscramble the Words")
        layout.addWidget(self.title_input)

        # Grid for inputs
        grid = QGridLayout()

        rows = 4
        cols = 3
        regex = QRegularExpression("^[A-Za-z]{0,12}$")
        validator = QRegularExpressionValidator(regex)

        for r in range(rows):
            for c in range(cols):
                word_input = EditableText(self.main_window)
                word_input.setPlaceholderText("word")
                word_input.setMaxLength(12)
                word_input.setValidator(validator)
                word_input.textChanged.connect(
                    lambda text, field=word_input: field.setText(text.lower())
                )
                self.word_inputs.append(word_input)

                grid.addWidget(word_input, r, c)

        layout.addLayout(grid)

        self.setLayout(layout)

    def get_words(self):

        words = []

        for field in self.word_inputs:
            text = field.text().strip()

            if text != "":
                words.append(text)

        return words

    def scramble_word(self, word):
        if len(word) <= 1:
                return word

        scrambled = word

        while scrambled == word:
            letters = list(word)
            random.shuffle(letters)
            scrambled = "".join(letters)

        return scrambled

    def get_scrambled_words(self):

        words = self.get_words()

        scrambled = []

        for word in words:
            scrambled.append(self.scramble_word(word))

        return scrambled

    def delete_section(self):
        if self in self.main_window.sections:
            self.main_window.sections.remove(self)

        self.setParent(None)

    def move_up(self):
        layout = self.main_window.section_layout
        index = layout.indexOf(self)

        if index > 0:
            # Move widget
            layout.removeWidget(self)
            layout.insertWidget(index - 1, self)
            # Move section in list
            sections = self.main_window.sections
            sections[index], sections[index - 1] = sections[index - 1], sections[index]

    def move_down(self):
        layout = self.main_window.section_layout
        index = layout.indexOf(self)
        if index < layout.count() - 1:
            layout.removeWidget(self)
            layout.insertWidget(index + 1, self)
            sections = self.main_window.sections
            sections[index], sections[index + 1] = sections[index + 1], sections[index]

    def get_size(self):
        words = self.get_scrambled_words()
        rows = (len(words) + 1) // 2
        return rows * 2

    def export(self, doc):
        words = self.get_scrambled_words()
        if not words:
            return

        rows = (len(words) + 1) // 2
        table = doc.add_table(rows=rows, cols=4)
        for i, word in enumerate(words):
            row = i % rows
            col = (i // rows) * 2
            table.rows[row].cells[col].text = f"{i+1}. {word}"
            table.rows[row].cells[col+1].text = "_______________________"
    
    def export_answers(self, doc):
        words = self.get_words()
        for i, word in enumerate(words, start=1):
            doc.add_paragraph(f"{i}. {word}")

    def get_title(self):
        return self.title_input.text()