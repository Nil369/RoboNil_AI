import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QWidget
from PyQt5.QtCore import Qt
from config import apikey

class QueryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.api_key = apikey # Replace this with your actual AI API key

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.input_line_edit = QLineEdit()
        self.input_line_edit.returnPressed.connect(self.process_query)

        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)

        layout.addWidget(self.input_line_edit)
        layout.addWidget(self.output_text_edit)

        self.central_widget.setLayout(layout)

    def process_query(self):
        query = self.input_line_edit.text()
        response = self.get_response_from_api(query)
        self.display_response(response)
        self.input_line_edit.clear()

    def get_response_from_api(self, query):
        
        api_endpoint = apikey  # Replace with your API endpoint
        headers = {"Authorization": "Bearer " + self.api_key}
        data = {"query": query}

        try:
            response = requests.post(api_endpoint, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"

    def display_response(self, response):
        self.output_text_edit.append("ChatBot: " + response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QueryApp()
    window.setWindowTitle("Query App")
    window.setGeometry(100, 100, 600, 400)
    window.show()
    sys.exit(app.exec_())
