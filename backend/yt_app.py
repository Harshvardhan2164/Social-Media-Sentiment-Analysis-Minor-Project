from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import joblib

app = Flask(__name__)
CORS(app, resources={r"/predictYT": {"origins": "http://localhost:3000"}})

classifier = joblib.load('lr_model.sav')
vectorizer = joblib.load('vectorizer.sav')
sentiments = SentimentIntensityAnalyzer()

@app.route('/predictYT', methods=["POST"])
def predict_sentimentYT():
        try:
        # Get the 'comment' from the request's JSON data
         data = request.get_json()
         comment = data['comment']

        # Preprocess the comment like in your original code
         cleaned_comment = ' '.join([w for w in comment.split() if len(w) > 3])
         cleaned_comment = cleaned_comment.lower()

        # Vectorize the cleaned comment
         comment_vector = vectorizer.transform([cleaned_comment]).toarray()

        # Predict sentiment using the classifier
         sentiment = classifier.predict(comment_vector)
         sentiment_maps = {0: "Neutral", -1: "Negative", 1:"Positive"}
         label = sentiment_maps[sentiment[0]]

        # Get sentiment scores using VADER
         vader_scores = sentiments.polarity_scores(cleaned_comment)

         return jsonify({'sentiment': label, 'vader_score': vader_scores})
        except Exception as e:
         return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
