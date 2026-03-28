from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QFrame
)
import re
from UI.utils.editable_text import EditableText
from UI.exports.formatting import add_text



class FillBlankSection(QFrame):

    def __init__(self, parent=None):
        super().__init__()
        
        self.main_window = parent
        self.questions = []
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                padding: 10px;
            }
        """)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Section title
        self.title_input = EditableText(self.main_window,"Fill in the Blanks")
        layout.addWidget(self.title_input)

        # Add questions
        self.question_input = EditableText(self.main_window)
        self.question_input.setPlaceholderText("Enter sentence...")
        self.question_input.setToolTip(
            "Place answers inside parentheses.\nExample: He (kicked) the ball."
        )
        layout.addWidget(self.question_input)

        # Add question button
        add_button = QPushButton("Add Question")
        add_button.clicked.connect(self.add_question)
        layout.addWidget(add_button)

        # Show Questions
        questions_title = QLabel("Questions Added:")
        questions_title.setStyleSheet("font-size:16px; font-weight:bold;")
        questions_title.setFixedHeight(40)
        layout.addWidget(questions_title)
        self.question_list = QListWidget()
        self.question_list.setFixedHeight(120)
        layout.addWidget(self.question_list)

        # Buttons to move and delete section
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        move_up = QPushButton("↑")
        move_down = QPushButton("↓")
        delete_button = QPushButton("Delete")

        move_up.setFixedWidth(40)
        move_down.setFixedWidth(40)
        delete_button.setFixedWidth(80)

        move_up.clicked.connect(self.move_up)
        move_down.clicked.connect(self.move_down)
        delete_button.clicked.connect(self.delete_section)

        button_layout.addWidget(move_up)
        button_layout.addWidget(move_down)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_question(self):
        text = self.question_input.text().strip()
        if text == "":
            return

        # Find answers
        answers = re.findall(r'\((.*?)\)', text)

        # Replace answers with blanks
        worksheet_text = re.sub(r'\((.*?)\)', "_____", text)

        # Create preview text
        if answers:
            answer_text = ", ".join(answers)
            preview = f"{worksheet_text} ({answer_text})"
        else:
            preview = worksheet_text

        # Store original sentence for export later
        self.questions.append(text)

        # Show preview in the list
        self.question_list.addItem(preview)

        self.question_input.clear()

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
        return len(self.questions) * 2

    def export(self, doc):
        for i, sentence in enumerate(self.questions, start=1):
            # Replace answers with blanks
            worksheet = re.sub(r'\((.*?)\)', "______________________", sentence)
            add_text(doc, f"{i}. {worksheet}")

    def export_answers(self, doc):
        for i, sentence in enumerate(self.questions, start=1):
            answers = re.findall(r'\((.*?)\)', sentence)
            answer_text = ", ".join(answers)
            doc.add_paragraph(f"{i}. {answer_text}")

    def get_title(self):
        return self.title_input.text()
    
    