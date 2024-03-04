import urllib
from transformers import AutoTokenizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from spellchecker import SpellChecker

import string
from pathlib import Path
import sys
base_dir = Path('/tensorfl_vision/deeplearning-app')
sys.path.append(str(base_dir))

class DataPreprocessing:
    def __init__(self):

       

        self.count = 0

        try:
            self.lemmatizer=WordNetLemmatizer()
            self.ensure_nltk_resources()
            self.stopwords = set(stopwords.words('english'))
            self.words = nltk.corpus.words.words()
            self.spell = SpellChecker()
            
            # load pretrained tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(base_dir / 'server_flask/models')
            


        except Exception as e:
            print(f"Error is occuring in INIT , due to {e}")
        
    def ensure_nltk_resources(self):
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/wordnet')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/words')

        except LookupError:

            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('stopwords')
            nltk.download('words')


    def preprocessingText(self, text):

        '''
            clean text from unncessary contents
        '''
        text = re.sub(r'http\S+', '', text) # remove urls
        text = re.sub(r'<.*?>', '', text) # remove tag
        text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
        text = text.lower() # convert to lowercasing

        # tokens
        tokens = nltk.word_tokenize(text)

        # spellchecking
        tokens = [ self.spell.correction(word) for word in tokens]

        if not tokens:
            print("****Empty, after spellchecking*****")
        # remove stopwords
        tokens  = [ word for word in tokens if word not in self.stopwords]

        if not tokens:
            print("****Empty After StopWords*****")
        # lemanize
        #tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        lemmanize_tokens = [self.lemmatizer.lemmatize(token) for token in tokens  if token and (token not in string.punctuation)]
      #  print (f"lemanize token {lemmanize_tokens} {self.count}")
        self.count+=1

        return ' '.join(lemmanize_tokens)



'''
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
    
    datapreprocessed =  DataPreprocessing()
    
    get_cleaned = datapreprocessed.preprocessingText(anger)
    
    print(f"cleaned text : > {get_cleaned}")
    
if __name__ == "__main__":
    main()
'''