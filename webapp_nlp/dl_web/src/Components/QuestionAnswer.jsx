import React, { useEffect, useRef, useState } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import "../Style/pdfViewer.css"
import axios from "axios"

import CustomChatComponent from "./CustomChatComponent";
import ChatBot from 'react-simple-chatbot';


function QuestionAnswer(){


  const [files, setFiles] = useState(null)



   // Additional state for forcing rerender
  const [chatKey, setChatKey] = useState(Math.random());
 

  const [showChatBot, setShowChatBot] = useState(false);

  
  const steps = [
    {
      id: '1',
      message: 'Ask Me all related to attached pdf?',
      trigger: 'question',
    },
    {
      id: 'question',
      component: <CustomChatComponent />,
      waitAction: true, // This tells the chatbot to wait until an action is performed to move to the next step
      // replace: true, // Uncomment if you want to replace the current step with the next one
    },
    // Define additional steps as needed
  ];
   


  const inputRef = useRef();

  //active movement
  const handleDragEnter = (event) =>{
    event.preventDefault();
    event.currentTarget.classList.add('active'); // Add the active class on drag enter
  }

  const handleDragLeave = (event) => {
    
    event.currentTarget.classList.remove('active'); // Remove the active class on drag leave
  };



  // handleDragover
  const handleDragOver = (event) =>{
    event.preventDefault()
  }


  // HANDLE PROCESS DRAG VS DROP
  const handleDrop = (event) => {
    event.preventDefault()
    processFiles(event.dataTransfer.files) // // Processes the dropped files

    // Remove the 'active' class to reset the dropzone's appearance
    event.currentTarget.classList.remove('active');
  };


  // Filters the selected files to include only PDFs and triggers the upload
  const processFiles = (selectedFiles) => {
   const filteredFiles = Array.from(selectedFiles).filter(

    (file) => file.type === "application/pdf"
   );

   if (filteredFiles.length > 0){
    setFiles(filteredFiles);// Updates the state with the filtered files
    uploadFiles(filteredFiles); // Upload files
   }
   else{
    alert("Only PDF files are accepted") // Alerts the user if no PDFs are selected
   }
  }

  // Either with button : Handle file selection via the file input element
  const handleChange = (event) =>{
    processFiles(event.target.files); // Processes the selected files
  }


  //UPLOADS SELECTED FILES TO SERVER
  const uploadFiles = (selectedFiles) =>{
    selectedFiles.forEach((file) => {

      const formData = new FormData();
      
      formData.append("file", file) /// Adds the file to the FormData object
      

      // MAKE POST REQUEST TO SERER OF FLASK
      try{
         axios.post('/content-analizer', formData, {
          headers:{
            "Content-Type":"multipart/form-data",// Sets the appropriate header for file upload
          },
        })
        .then((response) =>{
          console.log(response.data); //Logs server response
        })
        .catch((error)=>{
          console.error("Error uploading file : ", error); // Logs any error during the upload process
          //Aditinional error handling
        })
      }
      catch{
        console.log('Error try is not executed')
      }
    });
  }
     
  // display show chat bot
  const toggleChatBot =()=>{
    setShowChatBot(!showChatBot)
  }

  // return statment starts!
  return (

    <>

      <div className="dropzone"
       onDragOver = {handleDragOver}
       onDragEnter={handleDragEnter} 
       onDragLeave={handleDragLeave}
       onDrop ={handleDrop}
       
       >

        <h1>Drag and Drop PDF to Upload</h1>
        <h1>Or</h1>

      {/** INPUT TYPE OF HTML FILE*/}
        <input
        type='file'
        multiple
        onChange={handleChange}
        hidden
        accept='application/pdf'
        ref={inputRef}  
        >
      
        </input>

        <Button onClick={() => inputRef.current.click()} variant="dark" className='select-pdf'>Select PDF</Button>
        
        <Button onClick={toggleChatBot} variant="dark" style={{ marginTop: '20px' }} className='chatbotManage'>Toggle ChatBot</Button>
        
        </div>

        {showChatBot && (
          
          <ChatBot 
            key={chatKey}
            className='chat'
            headerTitle="AI BOT"
            steps={steps}
          />
        )}

    </>   

  ) 
   
}

export default QuestionAnswer;