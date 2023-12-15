import React from 'react'
import { useState } from 'react'
import axios from 'axios'

const YTSentimentAnalyzer =() => {
    const [input, setInput] = useState('')
    const [sentiment, setSentiment] = useState('')
    const [vader, setVader] = useState('')

    const handleInputChange = (e) =>{
        setInput(e.target.value)
    };

    const analyze = async()=>{
        try{
            const response = await axios.post('http://127.0.0.1:5000/predictYT', {
                comment: input,
            });
            console.log(response.data)
            setSentiment(response.data.sentiment)
            setVader(response.data.vader_score)
        }
        catch(error){
            console.error("Error: ", error)
        }

    }
  return (
    <div>
    <h2> YouTube Sentiment Analysis</h2>
    <textarea
      rows="4"
      cols="50"
      value={input}
      onChange={handleInputChange}
      placeholder="Enter a Comment"
    ></textarea>
    <button onClick={analyze}>Analyze Sentiment</button>
    {sentiment && <p>Predicted Sentiment: {sentiment}</p>}
    {vader && (
                <div>
                    <p>Vader Compound Score: {vader.compound}</p>
                    <p>Vader Negative Score: {vader.neg}</p>
                    <p>Vader Neutral Score: {vader.neu}</p>
                    <p>Vader Positive Score: {vader.pos}</p>
                </div>
            )}
  </div>
  )
}

export default YTSentimentAnalyzer