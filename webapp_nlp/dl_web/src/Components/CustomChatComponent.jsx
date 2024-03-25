// CustomChatComponent.jsx
import React, { useState } from 'react';
import axios from 'axios';

const CustomChatComponent = ({ steps, step, previousStep, triggerNextStep }) => {
  const [userInput, setUserInput] = useState('');
  const [answer, setAnswer] = useState('');

  const sendQuestion = async () => {
    if (!userInput.trim()) return;
    try {
      const response = await axios.post('/questions-chatbot', { question: userInput });
      const { data: { answer } } = response;
      setAnswer(answer);
      // Optionally trigger the next step if needed
      // triggerNextStep({ trigger: 'nextStepId' });
    } catch (error) {
      console.error("Error fetching answer:", error);
      setAnswer('Sorry, I could not fetch an answer.');
    }
  };

  return (
    <div>
      <input
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' ? sendQuestion() : null}
      />
      <button onClick={sendQuestion}>Send</button>
      {answer && <div>{answer}</div>}
    </div>
  );
};

export default CustomChatComponent;