from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.stem import PorterStemmer, WordNetLemmatizer
import joblib

app = Flask(__name__)
CORS(app, resources={r"/predictTweet": {"origins": "http://localhost:3000"}})

model = joblib.load('lr_model2.sav')
vectorizer = joblib.load('vectorizer2.sav')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

@app.route('/predictTweet', methods=['POST'])
def predict_sentiment():
    try:
        data=request.get_json()
        user_input = data['text']

        user_input = preprocess_text(user_input)
        user_input_vector = vectorizer.transform([user_input])

        sentiment = model.predict(user_input_vector)
        sentiment_mapping = {0: 'Negative', 2: 'Neutral', 4: 'Positive'}
        sentiment_label = sentiment_mapping[sentiment[0]]
        return jsonify({'sentiment': sentiment_label})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)