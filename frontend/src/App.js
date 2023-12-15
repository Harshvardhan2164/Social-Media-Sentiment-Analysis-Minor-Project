import SentimentAnalyzer from "./SentimentAnalyzer";
import YTSentimentAnalyzer from "./YTSentimentAnalyzer";
import AmazonSentimentAnalyzer from "./AmazonSentimentAnalyzer";
import React from "react";
import { Route, Routes, Link } from "react-router-dom";
function App() {
  return (
    <div>
        <li>
          <Link to="/Twitter">Twitter Analysis</Link>
        </li>
        <li>
          <Link to="/YouTube">YouTube Comment Analysis</Link>
        </li>
        <li>
          <Link to="/Amazon">Amazon Review Analysis</Link>
        </li>
        <Routes>
          <Route path="/" Component={SentimentAnalyzer}/>
          <Route exact path="/Twitter" Component={SentimentAnalyzer}/>
          <Route path="/YouTube" Component={YTSentimentAnalyzer}/>
          <Route path="/Amazon" Component={AmazonSentimentAnalyzer}/>
        </Routes>
      </div>
     
    
  );
}

export default App;
