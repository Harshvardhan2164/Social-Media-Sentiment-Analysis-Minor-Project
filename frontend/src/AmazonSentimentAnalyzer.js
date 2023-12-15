import React, {useState} from 'react'
import axios from 'axios'

const AmazonSentimentAnalyzer=()=> {
    const [UserInput, setUserInput] = useState('');
    const [Sentiment, setSentiment] = useState('');
    
    const handleInputChange = (e)=>{
        setUserInput(e.target.value);
    };
    const analyzeSentiment = async()=>{
        try{
            const response = await axios.post('http://127.0.0.1:5000/predictAmazon', {
                review: UserInput,
            });
            setSentiment(response.data.sentiment);
        }
        catch(error){
            console.error("Error: ", error);
        }
    };
  return (
    <div>
    <h2> Amazon Review Analysis</h2>
    <textarea
      rows="4"
      cols="50"
      value={UserInput}
      onChange={handleInputChange}
      placeholder="Enter a review"
    ></textarea>
    <button onClick={analyzeSentiment}>Analyze Sentiment</button>
    {Sentiment && <p>Predicted Sentiment: {Sentiment}</p>}
  </div>
  )
};

export default AmazonSentimentAnalyzer