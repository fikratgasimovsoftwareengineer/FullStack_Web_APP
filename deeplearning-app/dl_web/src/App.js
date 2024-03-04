import React from "react";

import IntegrateDl from "./Components/IntegrateDl";

import { BrowserRouter, Route, Routes } from 'react-router-dom';
import QuestionAnswer from "./Components/QuestionAnswer";
import EmotionAnalysis from "./Components/EmotionAnalysis";
function App() {
  return (
   
    
    <BrowserRouter>
    <Routes>
        <Route path="/" element={<IntegrateDl />} />
        <Route path="/emotionAnalysis" element={<EmotionAnalysis/>}/>
        <Route path="/questionAnswering" element={<QuestionAnswer/>}/>

        {/* Add more routes as needed */}
    </Routes>
</BrowserRouter>
  );
}

export default App;
