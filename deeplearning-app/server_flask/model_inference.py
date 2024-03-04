import torch

from transformers import  AutoTokenizer
import numpy as np
import sys
from pathlib import Path


base_dir = Path('/tensorfl_vision/deeplearning-app')
sys.path.append(str(base_dir))
from server_flask.algorithms.bert_sentiments import BertClassSentimentsLast
from server_flask.preprocessing.bert_preprocess import DataPreprocessing

class InferenceEmotions:
    
    def __init__(self):
        
    
        # private
        self.tokenizer = AutoTokenizer.from_pretrained(base_dir / 'server_flask/models')
        
        self.__encoded_dict = {'empty':1,'sadness':2, 'enthusiasm':3, 'neutral':4, 'worry':5, 'surprise':6,
                 'love':7, 'fun':8, 'hate':9, 'hapiness':10, 'boredom':11, 'relief':12, 'anger':13}
        
        self.decoded_dict = {v:k for k, v in self.__encoded_dict.items()}
        
        self.model = BertClassSentimentsLast()
        
        self.cleaning_text = DataPreprocessing()
        
        self.model.load_state_dict(torch.load(base_dir / 'server_flask/models/finetuned_model.pt'))
        #self.model.load_state_dict(torch.load(base_dir / 'updated_model/updated_bert.pt'), strict=False)
        self.model.eval()
        
    def predict(self, text, max_length=256):
        # FIRST, CLEAN TEXT 
        text = self.cleaning_text.preprocessingText(text)
        
        # tokenize OF CLEANED TEXT
        inputs = self.tokenizer(text, return_tensors='pt', max_length=max_length, truncation=True, padding="max_length")
            
        inputs_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
            
        with torch.no_grad():
            outputs  = self.model(inputs_ids, attention_mask)
                
        probabilities = torch.softmax(outputs, dim=1)
        
    
            
        predicted_class_id = torch.argmax(probabilities, dim=1).numpy()[0]
        
        
            
        predicted_class_probability = probabilities.numpy()[0][predicted_class_id]
        predicted_class_label = self.decoded_dict[predicted_class_id]

        return predicted_class_id, predicted_class_probability, predicted_class_label
        
    def get_embeddedings(self, text, max_length=256):
        # APPLY TOKENIZER TO CLEANED TEXT
        inputs = self.tokenizer(text, return_tensors='pt', max_length=max_length, truncation=True, padding="max_length")
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        
        with torch.no_grad():
            embeddings  = self.model(input_ids, attention_mask)
            
        return embeddings


def main():
    
    # bad
    sadness = "@gcrush @nopantsdance i was just thinking about how excited i am for you guys to move, but then i realized how sad i am to see you go."
   
    # optimal
    fun = "RIP leonardo. You were a great mini fiddler crab"
    
    # relief good
    worry = "My head hurts so bad I could scream!" # bad
    
    # bad
    surprise = "2 days of this month left, and I only have 400MB left on my onpeak downloads."
    
    # enthusiasm good
    enthusiasm  = "bed...sorta. today was good, sara has strep thought Angelina does to; i shared a water with her B4 they told me, i will prob get it to"
    
    # bad
    hate = "dammit! hulu desktop has totally screwed up my ability to talk to a particular port on one of our dev servers. so i can't watch and code"
    doInference = InferenceEmotions()
    
    hapiness = "@gcrush @nopantsdance i was just thinking about how excited i am for you guys to move, but then i realized how sad i am to see you go."
    
    
    # model UPDATE SHOWS PERFECT FOR ENTHUSIASM
    hapiness2 = "wants to hang out with friends SOON!"
    # model UPDATE SHOWS PERFECT GOOD FOR WORRY-?sadness
    worry = "Re-pinging @ghostridah14: why didn't you go to prom? BC my bf didn't like my friends"
    
    fear = " With everything , with everybody , with all this ! "
    joy = 'When I fell in love with \X\".  Overnight I felt confidence, self-esteem,    responsible and worthwhile."'
    fear2 = 'I was riding with a friend in his car. At a speed of 120 km/h on the snow-covered motorway I would have liked to get out.'
    anger = 'When you kill yourself with work and see the number of slakers wandering around, doing nothing.'
    # corrected emotion
    neutral = 'No problem , what class would you like to take ? '
    class_id, proba , class_name = doInference.predict(anger)
    
    print("Inference is doign...")
    
    print('\n')
    
    print("##########################")
    print("##########################")
    
    print(f"ID : {class_id} , probability {proba}, class name {class_name}")
    print('\n')
    print("##########################")
    print("##########################")
    
if __name__ == "__main__":
    main()
