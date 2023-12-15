from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import joblib

app = Flask(__name__)
CORS(app, resources={r"/predictTweet": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/predictYT": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/predictAmazon": {"origins": "http://localhost:3000"}})

model = joblib.load('lr_model2.sav')
vectorizer1 = joblib.load('vectorizer2.sav')
classifier = joblib.load('lr_model.sav')
vectorizer = joblib.load('vectorizer.sav')
amaz_model=joblib.load('amazon_model.sav')
amaz_vectorizer=joblib.load('amazon_vectorizer.sav')

sentiments = SentimentIntensityAnalyzer()

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stop_words = stopwords.words('english')

def clean_review(review):
    review = " ".join(word for word in review.split() if word not in stop_words)
    return review

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
        user_input_vector = vectorizer1.transform([user_input])

        sentiment = model.predict(user_input_vector)
        sentiment_mapping = {0: 'Negative', 2: 'Neutral', 4: 'Positive'}
        sentiment_label = sentiment_mapping[sentiment[0]]
        return jsonify({'sentiment': sentiment_label})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predictYT', methods=["POST"])
def predict_sentimentYT():
        try:
        
         data = request.get_json()
         comment = data['comment']

        
         cleaned_comment = ' '.join([w for w in comment.split() if len(w) > 3])
         cleaned_comment = cleaned_comment.lower()

        
         comment_vector = vectorizer.transform([cleaned_comment]).toarray()

        
         sentiment = classifier.predict(comment_vector)
         sentiment_maps = {0: "Neutral", -1: "Negative", 1:"Positive"}
         label = sentiment_maps[sentiment[0]]

        
         vader_scores = sentiments.polarity_scores(cleaned_comment)

         return jsonify({'sentiment': label, 'vader_score': vader_scores})
        except Exception as e:
         return jsonify({'error': str(e)})

@app.route('/predictAmazon', methods=["POST"])
def predict_sentimentAmazon():
    try:
        data=request.get_json()
        review = data['review']

        cleaned_review = clean_review(review)
        review_vector= amaz_vectorizer.transform([cleaned_review]).toarray()
        sentiment = amaz_model.predict(review_vector)
        sentiment_labels={0:'Negative', 1: 'Positive'}
        label = sentiment_labels[sentiment[0]]
        return jsonify({'sentiment': label})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)