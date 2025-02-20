from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from googletrans import Translator
import joblib

app = Flask(__name__)
CORS(app, resources={r"/predictTweet": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/predictYT": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/predictAmazon": {"origins": "http://localhost:3000"}})

model = joblib.load('twitter_acc_model.sav')
vectorizer1 = joblib.load('twitter_acc_vectorizer.sav')
classifier = joblib.load('lr_model.sav')
vectorizer = joblib.load('vectorizer.sav')
amaz_model=joblib.load('amazon_acc_model.sav')
amaz_vectorizer=joblib.load('amazon_acc_vectorizer.sav')

sentiments = SentimentIntensityAnalyzer()

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
translator = Translator()

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
        user_input = translator.translate(user_input, src='auto', dest='en').text
        cleaned_tweet = ' '.join([w for w in user_input.split() if len(w) > 3])
        cleaned_tweet= cleaned_tweet.lower()
        tweet_vector = vectorizer1.transform([cleaned_tweet]).toarray()
        sentiment = model.predict(tweet_vector)
        sentiment_mapping = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
        sentiment_label = sentiment_mapping[sentiment[0]]
        vader_scores = sentiments.polarity_scores(cleaned_tweet)
        return jsonify({'sentiment': sentiment_label, 'vader_score': vader_scores})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predictYT', methods=["POST"])
def predict_sentimentYT():
        try:
        
         data = request.get_json()
         comment = data['comment']

         comment = translator.translate(comment, src='auto', dest='en').text
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
        review = translator.translate(review, src='auto', dest='en').text
        cleaned_review = ' '.join([w for w in review.split() if len(w) > 3])
        review_vector= amaz_vectorizer.transform([cleaned_review]).toarray()
        sentiment = amaz_model.predict(review_vector)
        sentiment_labels={0: "Neutral", -1: "Negative", 1:"Positive"}
        label = sentiment_labels[sentiment[0]]
        vader_scores = sentiments.polarity_scores(cleaned_review)
        return jsonify({'sentiment': label, 'vader_score': vader_scores})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)