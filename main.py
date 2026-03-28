import sys
from wsgiref import headers
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QCheckBox,
    QLabel, QScrollArea, QMenu, QSpinBox, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import QPoint
from UI.sections.fill_blanks import FillBlankSection
from UI.sections.unscramble import UnscrambleSection
from UI.exports.docx_export import export_document, export_answers
from UI.sections.word_search import WordSearchSection
from UI.utils.editable_text import EditableText

class WorksheetGenerator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Worksheet Generator")
        self.setGeometry(200, 200, 700, 600)
        self.setStyleSheet("background:#f5f5f5;")
        self.sections = []
        self.active_text_widget = None

        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("""
            QPushButton {
                background: #0078d7;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 16px;
                font-size: 15px;
            }
            QPushButton:pressed {
                background: #005fa3;
            }
            QPushButton:checked {
                background: #005fa3;
            }
            QLabel {
                color: #222;
            }
            QSpinBox, QComboBox {
                border: 1.5px solid #d0d0d0;
                border-radius: 6px;
                padding: 4px 8px;
                background: #fafbfc;
                font-size: 15px;
            }
            QSpinBox:focus, QComboBox:focus {
                border: 1.5px solid #0078d7;
                background: #fff;
            }
            QCheckBox {
                font-size: 15px;
                color: #222;
                spacing: 8px;
            }

            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1.5px solid #d0d0d0;
                background: #fafbfc;
            }

            QCheckBox::indicator:hover {
                border: 1.5px solid #0078d7;
            }

            QCheckBox::indicator:checked {
                background-color: #0078d7;
                border: 1.5px solid #0078d7;
            }

            QCheckBox::indicator:checked:hover {
                background-color: #005fa3;
                border: 1.5px solid #005fa3;
            }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()

        toolbar = QHBoxLayout()

        self.font_size = QSpinBox()
        self.font_size.setRange(6, 72)
        self.font_size.setValue(12)

        self.bold_button = QPushButton("B")
        self.bold_button.setCheckable(True)

        self.italic_button = QPushButton("I")
        self.italic_button.setCheckable(True)

        self.underline_button = QPushButton("U")
        self.underline_button.setCheckable(True)

        self.font_size.valueChanged.connect(self.change_font_size)
        self.bold_button.clicked.connect(self.toggle_bold)
        self.italic_button.clicked.connect(self.toggle_italic)
        self.underline_button.clicked.connect(self.toggle_underline)

        toolbar.addWidget(self.font_size)
        toolbar.addWidget(self.bold_button)
        toolbar.addWidget(self.italic_button)
        toolbar.addWidget(self.underline_button)
        main_layout.addLayout(toolbar)

        title_label = QLabel("Worksheet Title:")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(title_label)

        self.title_input = EditableText(self)
        main_layout.addWidget(self.title_input)

        # ✅ NEW: Header options (Name / Date / Class)
        header_layout = QHBoxLayout()

        self.name_checkbox = QCheckBox("Name")
        self.date_checkbox = QCheckBox("Date")
        self.class_checkbox = QCheckBox("Class")

        header_layout.addWidget(self.name_checkbox)
        header_layout.addWidget(self.date_checkbox)
        header_layout.addWidget(self.class_checkbox)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Scroll area for sections
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.section_container = QWidget()
        self.section_layout = QVBoxLayout()
        self.section_layout.setSpacing(15)

        self.section_container.setLayout(self.section_layout)
        self.scroll.setWidget(self.section_container)

        main_layout.addWidget(self.scroll)

        # Add section button
        self.add_section_button = QPushButton("Add Section")
        self.add_section_button.clicked.connect(self.show_section_menu)

        # Export button
        self.export_button = QPushButton("Export Worksheet")
        self.export_button.clicked.connect(self.export_worksheet)

        main_layout.addWidget(self.add_section_button)
        main_layout.addWidget(self.export_button)

        main_widget.setLayout(main_layout)

    def show_section_menu(self):

        menu = QMenu()
        menu.setStyleSheet("""
        QMenu {
            background: #fafbfc;
            border: 1.5px solid #d0d0d0;
            border-radius: 8px;
            padding: 6px;
            font-size: 15px;
        }
        QMenu::item {
            padding: 8px 20px;
            border-radius: 5px;
        }
        QMenu::item:selected {
            background: #0078d7;
            color: white;
        }
        """)

        fill_action = menu.addAction("Fill in the Blanks")
        unscramble_action = menu.addAction("Unscramble Words")
        wordsearch_action = menu.addAction("Word Search")

        button_pos = self.add_section_button.mapToGlobal(
            self.add_section_button.rect().topRight()
        )

        menu_height = menu.sizeHint().height()

        # Move menu above the button
        pos = QPoint(button_pos.x(), button_pos.y() - menu_height)

        action = menu.exec(pos)

        if action == fill_action:
            self.add_fill_section()

        elif action == unscramble_action:
            self.add_unscramble_section()

        elif action == wordsearch_action:
            self.add_wordsearch_section()

    def add_fill_section(self):
        section = FillBlankSection(self)
        self.sections.append(section)
        self.section_layout.insertWidget(
            self.section_layout.count(), section
        )

    def add_unscramble_section(self):
        section = UnscrambleSection(self)
        self.sections.append(section)
        self.section_layout.insertWidget(
            self.section_layout.count(), section
        )

    def add_wordsearch_section(self):
        section = WordSearchSection(self)
        self.sections.append(section)
        self.section_layout.insertWidget(
            self.section_layout.count(), section
        )

    def export_worksheet(self):
        title = self.title_input.text()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Worksheet",
            "",
            "Word Document (*.docx)"
        )
        if not file_path:
            return

        if not file_path.endswith(".docx"):
            file_path += ".docx"

        headers = self.get_selected_headers()
        export_document(title, self.sections, file_path, headers=headers)
        answer_path = file_path.replace(".docx", "_answers.docx")
        export_answers(title, self.sections, answer_path)

    def set_active_text(self, widget):
        self.active_text_widget = widget
        font = widget.font()
        self.font_size.setValue(font.pointSize())
        self.bold_button.setChecked(font.bold())
        self.italic_button.setChecked(font.italic())
        self.underline_button.setChecked(font.underline())

    def change_font_size(self, size):
        if not self.active_text_widget:
            return

        font = self.active_text_widget.font()
        font.setPointSize(size)
        self.active_text_widget.setFont(font)

    def toggle_bold(self):
        if not self.active_text_widget:
            return

        font = self.active_text_widget.font()
        font.setBold(self.bold_button.isChecked())
        self.active_text_widget.setFont(font)

    def toggle_italic(self):
        if not self.active_text_widget:
            return

        font = self.active_text_widget.font()
        font.setItalic(self.italic_button.isChecked())
        self.active_text_widget.setFont(font)

    def toggle_underline(self):
        if not self.active_text_widget:
            return

        font = self.active_text_widget.font()
        font.setUnderline(self.underline_button.isChecked())
        self.active_text_widget.setFont(font)

    def get_selected_headers(self):
        headers = []

        if self.name_checkbox.isChecked():
            headers.append("Name")
        if self.date_checkbox.isChecked():
            headers.append("Date")
        if self.class_checkbox.isChecked():
            headers.append("Class")

        return headers





def main():
    app = QApplication(sys.argv)
    window = WorksheetGenerator()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()