import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.controllers.main_controller import process_notion_to_hatena


class WorkerThread(QThread):
    finished_signal = Signal(str)
    error_signal = Signal(str)

    def __init__(self, url_or_id, publish):
        super().__init__()
        self.url_or_id = url_or_id
        self.publish = publish

    def run(self):
        try:
            process_notion_to_hatena(self.url_or_id, self.publish)
            self.finished_signal.emit("Successfully posted to Hatena Blog!")
        except Exception as e:
            self.error_signal.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notion to Hatena")

        # Main layout
        layout = QVBoxLayout()

        # URL/ID Input
        self.url_label = QLabel("Notion Page URL or ID:")
        layout.addWidget(self.url_label)
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        # Publish Checkbox
        self.publish_checkbox = QCheckBox("Publish directly (default is draft)")
        layout.addWidget(self.publish_checkbox)

        # Execute Button
        self.execute_button = QPushButton("Execute")
        self.execute_button.clicked.connect(self.on_execute)
        layout.addWidget(self.execute_button)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Adjust size to fit content
        self.adjustSize()

        # Fix height, allow width resizing
        self.setFixedHeight(self.height())
        self.setMinimumWidth(300)

    def on_execute(self):
        url_or_id = self.url_input.text().strip()
        if not url_or_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Notion Page URL or ID.")
            return

        publish = self.publish_checkbox.isChecked()

        # Disable button while processing
        self.execute_button.setEnabled(False)
        self.execute_button.setText("Processing...")

        # Start worker thread
        self.worker = WorkerThread(url_or_id, publish)
        self.worker.finished_signal.connect(self.on_success)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def on_success(self, message):
        self.execute_button.setEnabled(True)
        self.execute_button.setText("Execute")
        QMessageBox.information(self, "Success", message)

    def on_error(self, message):
        self.execute_button.setEnabled(True)
        self.execute_button.setText("Execute")
        QMessageBox.critical(self, "Error", f"An error occurred:\n{message}")


def launch_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
