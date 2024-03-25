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

base_dir = Path('/tensorfl_vision/webapp_nlp')
sys.path.append(str(base_dir))



from server_flask.model_inference import InferenceEmotions
from server_flask.llm_pdf.llm_transformer2 import ContentAnalyzer2

class DLServer:
    
    
    def __init__(self):
        
        
        self.app = Flask(__name__)
        
        self.app.secret_key = 'serverreact'
        
        CORS(self.app)
    
        # Define a directory for saving uploaded files
        # Make sure this directory exists and is writable
        self.pdf_folder = base_dir / 'server_flask/data/output_pdf'
        if not os.path.exists(self.pdf_folder):
            os.makedirs(self.pdf_folder, exist_ok=True)
    
        
        # route for pdf analyze 
        self.app.add_url_rule('/content-analizer', view_func=self.postprocess_pdf, methods=['POST'])
        
        # route user pdf related questions
        self.app.add_url_rule('/questions-chatbot', view_func=self.handleUserInputChat, methods=['POST'])
        
        # route for text analysis
        self.app.add_url_rule('/analyze-text', view_func=self.postprocessing_on_text, methods=['POST'])
        
        # user feedback 
        self.app.add_url_rule('/user-feedback', view_func = self.handle_feedback, methods=['POST'])
    
        self.doInference = InferenceEmotions()
        
        self.pdfAnalizerChat = ContentAnalyzer2()
        
        self.predicted_emotion = ''
        
        self.feedback_file = 'user_feedback.csv'
        self.abs_path = base_dir / 'server_flask/data'
        self.feedback_asb = os.path.join(self.abs_path,self.feedback_file)
        
        self.chunks = None
        
        self.init_feedback_file()
    
    def init_feedback_file(self):
        
        if not os.path.exists(self.feedback_asb) or os.path.getsize(self.feedback_asb) == 0:
            with open(self.feedback_asb, mode='w', newline='') as file:
                writer = csv.DictWriter(file,fieldnames=["predicted_emotion", "use_defined_emotion", "original_text"])
                writer.writeheader()
        
    
    def postprocess_pdf(self):
        
        # check if post request hjas file part
        # 400 indicates that client side data has not been recieved succesfull!
        if 'file' not in request.files:
            return jsonify({"error":"No file part in the request"}), 400
        
        # get file
        file = request.files['file']
        
        # user does not submit file or file is empty content
        if file.filename == '':
            return jsonify({'error':'No selected file'}), 400
        
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(self.pdf_folder,  filename)
            
            # save file
            file.save(save_path)
            # Optionally, process the file here
            # Postprocessd pdf
            self.pdfAnalizerChat.extract_text_from_pdf(save_path)
        
            ## postprocess file
            
            # return succesful message
            return jsonify({'message':f'File {filename} uploaded successfully'}), 200
        else:
            return jsonify({'error':'Invalid file type'}), 400
        
    
    def handleUserInputChat(self):
        data = request.json
        question = data.get('question')
        
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        #print(self.chunks)
        # answer 
        answer = self.pdfAnalizerChat.find_best_answer(question)
        
        
        if answer:
            print(f"Answer is :", answer)
            
            return jsonify({"answer":answer}), 200
        else:
            return jsonify({"error":"Unable to find answer"}), 404
        
    def allowed_file(self, filename):
        
        # check if file extension is allowed
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
        
    
    
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
            writer = csv.DictWriter(file, fieldnames=
                ["predicted_emotion",
                 "use_defined_emotion",
                 "original_text"])
            
            
            writer.writerow({
                "predicted_emotion": predicted_emotion,
                "use_defined_emotion": correct_emotion,
                "original_text" :  original_text
            })
        
       
if __name__ == '__main__':
    server = DLServer()
    server.app.run(debug=True)
   
            