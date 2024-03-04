import sys
from pathlib import Path
from flask import Flask, json, session, request, flash, jsonify
from flask import redirect

from flask_cors import CORS
from werkzeug.utils import secure_filename
import csv
import os
import sys
from pathlib import Path

base_dir = Path('/tensorfl_vision/deeplearning-app')
sys.path.append(str(base_dir))



from server_flask.model_inference import InferenceEmotions

class DLServer:
    
    
    def __init__(self):
        
        
        self.app = Flask(__name__)
        
        self.app.secret_key = 'serverreact'
        
        CORS(self.app)
        # route for text analysis
        self.app.add_url_rule('/analyze-text', view_func=self.postprocessing_on_text, methods=['POST'])
        
        # user feedback 
        self.app.add_url_rule('/user-feedback', view_func = self.handle_feedback, methods=['POST'])
    
        self.doInference = InferenceEmotions()
        
        self.predicted_emotion = ''
        
        self.feedback_file = 'user_feedback.csv'
        self.abs_path = base_dir / 'server_flask/data'
        self.feedback_asb = os.path.join(self.abs_path,self.feedback_file)
        
        self.init_feedback_file()
    
    def init_feedback_file(self):
        
        if not os.path.exists(self.feedback_asb) or os.path.getsize(self.feedback_asb) == 0:
            with open(self.feedback_asb, mode='w', newline='') as file:
                writer = csv.DictWriter(file,fieldnames=["predicted_emotion", "use_defined_emotion", "original_text"])
                writer.writeheader()
        
    
    def postprocessing_on_text(self):
        
        # Get text from the request
       # If the mimetype is application/json this will contain the parsed JSON data.
        
        getData = request.json
        self.getText = getData.get('text', '')
            
        if not self.getText:
            return({'Error' : "No text provided"}), 400
            
            # Use your model to process the text
        class_id, probability, class_name = self.doInference.predict(self.getText)

        self.predicted_emotion = class_name
            # convert numpy int64 to python int before returning
        class_id = int(class_id) # Convert class_id to Python native type
        probability = float(probability) # Ensure probability is also serializable; usually it's a float so this might be redundant
            
        return jsonify({
                'class_id':class_id,
                'probability':probability,
                'class_name':class_name
        })
        
    def handle_feedback(self):
        
        data = request.json
        print(data)
        original_text = self.getText
        correct_emotion = data['correct_emotion']
        print("-----------------")
        print( original_text, correct_emotion)
        self.save_feedback(self.predicted_emotion, correct_emotion, original_text)
        
        return jsonify({"message":"Feedback received"}), 200
        
        
    def save_feedback(self, predicted_emotion, correct_emotion,  original_text):
        
        # append the feedback
        with open(self.feedback_asb , mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["predicted_emotion", "use_defined_emotion", "original_text"])
            writer.writerow({
                "predicted_emotion": predicted_emotion,
                "use_defined_emotion": correct_emotion,
                "original_text" :  original_text
            })
        
       
if __name__ == '__main__':
    server = DLServer()
    server.app.run(debug=True)
   
            