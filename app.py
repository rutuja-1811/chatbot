from flask import Flask, render_template, request, jsonify
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextBrowser, QListWidget, QListWidgetItem, QMessageBox, QLabel
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from docx import Document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    # Replace this with your logic to process the user_message
    bot_response = "This is a sample response from the Python chatbot."
    return jsonify({'botResponse': bot_response})

class ChatbotGUI(QWidget):
    def __init__(self, docx_file):
        super().__init__()
        self.docx_file = docx_file
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RP hit Chatbot')
        self.setGeometry(100, 100, 800, 400)

        # Layouts
        main_layout = QHBoxLayout()

        # User's query history
        history_layout = QVBoxLayout()

        # Title for the history
        history_title = QLabel("History")
        history_title.setAlignment(Qt.AlignCenter)
        history_title.setStyleSheet("background-color: #E0E0E0; font-size: 16px; font-weight: bold; padding: 5px;")
        history_layout.addWidget(history_title)

        self.query_history = QListWidget(self)
        self.query_history.setStyleSheet("background-color: #F5F5F5; color: #000000; font-size: 16px;")
        self.query_history.setMaximumWidth(200)
        history_layout.addWidget(self.query_history)

        main_layout.addLayout(history_layout)

        # Chat display
        chat_layout = QVBoxLayout()

        # Title for the query response
        response_title = QLabel("RP Hit")
        response_title.setAlignment(Qt.AlignCenter)
        response_title.setStyleSheet("background-color: #E0E0E0; font-size: 16px; font-weight: bold; padding: 5px;")
        chat_layout.addWidget(response_title)

        self.chat_display = QTextBrowser(self)
        font = QFont("Courier New", 16)
        self.chat_display.setFont(font)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")
        chat_layout.addWidget(self.chat_display)

        # User input
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type your message...")
        self.input_box.returnPressed.connect(self.on_send_clicked)
        self.input_box.setStyleSheet("color: #000000; background-color: #FFFFFF; border: 1px solid #707070; font-size: 16px;")
        input_layout.addWidget(self.input_box)

        # Send button
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.on_send_clicked)
        input_layout.addWidget(self.send_button)

        chat_layout.addLayout(input_layout)
        main_layout.addLayout(chat_layout)

        self.setLayout(main_layout)

        # Connect itemClicked signal to a slot
        self.query_history.itemClicked.connect(self.on_query_clicked)

    def on_send_clicked(self):
        # Get user input
        user_question = self.input_box.text()

        # Get response from the chatbot (read data from DOCX file)
        bot_response = self.get_bot_response(user_question)

        # Display user question and bot response with different colors
        self.display_chat(user_question, bot_response)

        # Add the user question to the query history
        self.add_to_query_history(user_question)

        # Clear the input box
        self.input_box.clear()

    def add_to_query_history(self, query):
        # Add the query to the query history list
        item = QListWidgetItem(query)
        self.query_history.addItem(item)

    def on_query_clicked(self, item):
        # Retrieve information based on the clicked query in history
        query = item.text()
        bot_response = self.get_bot_response(query)

        # Display the information in a popup
        QMessageBox.information(self, 'Query History', f'Query: {query}\nBot Response: {bot_response}')

    def get_bot_response(self, user_question):
        # Replace this with your logic to fetch information based on user_question from DOCX file
        doc = Document(self.docx_file)

        for row in doc.tables[0].rows:
            question = row.cells[0].text
            answer = row.cells[1].text
            if user_question.lower() in question.lower():
                return answer

        return 'I do not have information on that.'

    def display_chat(self, user_question, bot_response):
        # Display the conversation in the QTextBrowser
        self.chat_display.append(f'User: {user_question}')
        self.chat_display.append(f'Bot: {bot_response}')
        self.chat_display.append('')

if __name__ == '__main__':
    # Specify the path to your DOCX file
    docx_file_path = "C:\\Users\\DELL\\Desktop\\chatbot.docx"

    app = QApplication(sys.argv)
    window = ChatbotGUI(docx_file_path)
    window.show()
    sys.exit(app.exec_())
