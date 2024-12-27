# app.py


from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

app = Flask(__name__)

class TicketClassifier:
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()

    def preprocess_data(self, ticket_data):
        texts, categories = zip(*ticket_data)
        X = self.vectorizer.fit_transform(texts)
        y = np.array(categories)
        return X, y

    def train_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict_category(self, text):
        text_vectorized = self.vectorizer.transform([text])
        category = self.model.predict(text_vectorized)[0]
        return category

# Mock data for ticket history
ticket_history = [
    ("Issue with login page", "Technical"),
    ("Cannot access the database", "Technical"),
    ("Request for new software installation", "Request"),
    ("Printer not working", "Technical"),
    ("Password reset request", "Request"),
    ("Billing inquiry", "Billing"),
]

# Initialize the ticket classifier and train the model
ticket_classifier = TicketClassifier()
X, y = ticket_classifier.preprocess_data(ticket_history)
ticket_classifier.train_model(X, y)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    ticket_text = request.form['ticket_text']
    predicted_category = ticket_classifier.predict_category(ticket_text)
    return render_template('result.html', ticket_text=ticket_text, category=predicted_category)

if __name__ == '__main__':
    app.run(debug=True)
