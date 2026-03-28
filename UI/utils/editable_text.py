from PyQt6.QtWidgets import QLineEdit

class EditableText(QLineEdit):

    def __init__(self, main_window, text=""):
        super().__init__(text)
        self.main_window = main_window
        self.setStyleSheet("""
            QLineEdit {
                background: #fafbfc;
                border: 1.5px solid #d0d0d0;
                border-radius: 6px;
                padding: 6px 10px;
                transition: border-color 0.2s;
            }
            QLineEdit:focus {
                border: 1.5px solid #0078d7;
                background: #ffffff;
            }
        """)

    def focusInEvent(self, event):
        self.main_window.set_active_text(self)
        super().focusInEvent(event)