import React from "react";

import 'bootstrap/dist/css/bootstrap.min.css';

import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';

import { data_images } from './DataCompact'
import Button from 'react-bootstrap/Button';
import { useNavigate } from "react-router-dom";

import '../Style/integratedl.css'


function IntegrateDl() {

  const navigate = useNavigate();
  

  // navigate to component path
  const navigateToComponent = (componentPath) => {
    navigate(componentPath);
  }


  return (
      <CardGroup className="card-container">
          {data_images.map((item) => {
          
              let cardTitle;
              let className;
              let button_inference;
              let componentPath;

              if (item.id === 1) {

                 
                  cardTitle = "Question & Answering";
                  className = 'disaster-tweet'
                  button_inference = 'Start Classification Inference'
                  componentPath = '/questionAnswering';

              } else if (item.id === 2) {
                
                
                  cardTitle = "Emotion Detection from Text";
                  className = 'emotion-tweet';
                  button_inference = 'Start Emotion Detection Inference';
                  componentPath = "/emotionAnalysis"; // Update with the correct path

              }

              return (
                  <Card key={item.id} style={{ width: '20rem', margin: '20px' }} className={className}>
                      <Card.Img variant="top" src={item.image} className="card-sentiment" />
                      <Card.Body>
                        <div className="text-title">
                          <Card.Title>{cardTitle}</Card.Title>
                          <Card.Text>
                              This is a card with supporting text below as a natural lead-in to additional content.
                          </Card.Text>
                          </div>
                        
                      </Card.Body>
                      <div>
                        <Button  className="btn-id" onClick={()=>navigateToComponent(componentPath)}>{button_inference}</Button>
                      </div>
                  </Card>
                 
              );
             
          })}
        
      </CardGroup>
      
  );
}

export default IntegrateDl;