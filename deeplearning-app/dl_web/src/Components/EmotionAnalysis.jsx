import React, { useState } from "react";
import Form from 'react-bootstrap/Form';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Style/EmotionAnalysis.css'
import ProgressBar from 'react-bootstrap/ProgressBar';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import { Pie } from "react-chartjs-2";
import Dropdown from 'react-bootstrap/Dropdown';

import {Chart, ArcElement, Tooltip, Legend} from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend);

function EmotionAnalysis(){

    // State management code here
    // text retuirn to text area
    // POST DATA TO ROUTE
    const [emotionText, setEmotionText] = useState('');

    // userreponse and feedback
    const[userFeedBack, setUserFeedBack] = useState('');

    // SUBMIT USER INPUT TRACK RECIEVED DATA AND SET TO TEXT AREA
    const [submitUserInput, setSubmitUserInput] = useState('');
    

    // SET EMOTIONS COUNT LIST
    const [emotionCounts, setEmotionCounts] = useState({});
    
    // SET EMOTIONS COUNT ARRAY
    const [collectTexts, setCollectTexts] = useState([]);

      
    /**State Mangemetn for validation of pier chart visibility */

    const [showPieChart, setShowPieChart] = useState(false);


    // track progrsss bar

    const [progress, setProgress] = useState(0);

    // text retuirn to text area

    const trackOutputChange = (event) => {
        setEmotionText(event.target.value);
    }

    // handle user feedback change 
    const handleUserFeedBackChange = (event) =>{
        setUserFeedBack(event.target.value) // update the user feedback
    }

   
   
        /*post data to server and recieved data from server*/ 
    const submitHandler = async() =>{
        const keyPhrase = "my choice is";
        const trimmetText = emotionText.trim() // entire uwhole sentence
        console.log(`keyPhrase ${keyPhrase }`)
        console.log('-----------------------')
        console.log(`${trimmetText} trimmed text }`)
        
        console.log(`${trimmetText.toLocaleLowerCase()} trimmed text 2 }`)
        if (trimmetText.toLocaleLowerCase().startsWith(keyPhrase)){
            // emotion start index
            const emotionStartIndex = keyPhrase.length;
            //get emotion name
            // get difference between start and end index
            const correctEmotion = trimmetText.slice(emotionStartIndex).trim();
            try{
     // Assuming you have the original text stored or you ask users to include it again
                    await axios.post('/user-feedback',{

                    original_text : emotionText,
                    correct_emotion: correctEmotion
                });

                
                alert('Feedback Submited successfully');
                setEmotionText('');
                setProgress(0);
            }
                catch (error) {
                    console.error('Error submitting feedback:', error);
                    alert("Error submitting feedback");
            }
           
        }else{



        setProgress(10); // Initialize progress to 10% to indicate start
        try {

            const response = await axios.post('/analyze-text', {text:emotionText});

            setProgress(70);
            /*HERE AXIOS WAIT  ANSWERED FROM MODEL!*/ 
            ////##################################
            // submit text button
            setSubmitUserInput(
                `MODEL INFERENCE OUTPUT : 
                =========================
               # Detected Class ID ${response.data.class_id}
               # Probability ${response.data.probability.toFixed(2)}
               # Class Name ${response.data.class_name} 
                ==========================
                `);
            setProgress(100);
            setTimeout(() => setProgress(0), 500);

            // set response.data.class_name as key and value pair
            // || will return 0 if class name is not ofund otherswise
            setEmotionCounts(prevCounts=>({
            ...prevCounts,
           [response.data.class_name]:(prevCounts[response.data.class_name] || 0) + 1
           }))

        // collect texts
           setCollectTexts(prevTexts=>[...prevTexts, emotionText])
       
                               
        }catch(error){
            console.error('Error On Text Generation');
            setSubmitUserInput('Error on Analyzing text. Please try again...')
        }
    }
}

 
    // Simplified CSV download function
    const downloadTextsAsCSV = () => {
        const csvContent = "data:text/csv;charset=utf-8," + collectTexts.map(e => e.replace(/"/g, '""')).join("\n");
        const encodedUri = encodeURI(csvContent);
        window.open(encodedUri);
    };

    //Dummy data

    // Dummy data for the pie chart
    const data = {
        labels: Object.keys(emotionCounts),
        datasets: [{
            data: Object.values(emotionCounts),
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56','#3b0b36','#17d13c'],
            hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56','#3b0b36','#17d13c']
        }]
    
    };
        // Add options to configure the legend.
    const options = {
        plugins: {
            legend: {
                display: true, // Ensure the legend is displayed
                position: 'top', // You can change this as needed
            }
        },
        // Additional configurations can go here
    };

    //event handler for triggering pier chrat
    const togglePieChart = () => setShowPieChart(!showPieChart);



    return ( 
       <>
            <div className="sidebar-content">
                <h4>Emotions Content Menu</h4>
                <hr/>

                <ul>
                    <li className="align-buttons">
                        <button className="emotion-analytics" onClick={togglePieChart }>
                            <span>Emotions Analytics</span>
                        </button>
                        <br></br>
                        
                        <button className="buffer-data" onClick={downloadTextsAsCSV}>
                            <span>Visualize all Inputs</span>
                        </button>
                    </li>
                </ul>
            </div>
          
            <Form className="textArea-explanation">
                <Form.Group className="mb-3 emotion-textarea" controlId="emotionTextarea">
                    <Form.Label> Emotion Detection </Form.Label> {/*placeholder="Wait For Model response..."*/}
                    <Form.Control as="textarea"  value={submitUserInput}  rows={8} className="textArea-Color" />
                    <ProgressBar  striped variant="danger" now={progress} label={`${progress}%`} />
                </Form.Group>
                
                <div className="input-emotion">
                    <Form.Label>Enter Emotional Text</Form.Label>
                    
                        <Form.Control
                                type="text"
                                id="inputPassword5"
                                aria-describedby="textInput"
                                onChange={trackOutputChange}  // Make sure to update the state on change

                        />
               
        

                        {/**button is starting asyronous submit and recieves data simulatenously */}
                      <div className='submit-button'>
                        <Button variant="info" onClick={submitHandler}>Send Message</Button>
                      </div>
                </div>
                
              
            </Form>
           
            
            <div className="design-piechart">
                {showPieChart && (
                    <div >
                        <Pie data={data} options ={options} />
                    </div>
                )}
            </div>
        
     </>
       
    )
}

export default EmotionAnalysis;