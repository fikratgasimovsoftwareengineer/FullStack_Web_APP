import torch
from torch import nn, optim
import torch.nn.functional as F
from collections import deque, namedtuple
import random
import sys
from pathlib import Path
import pandas as pd
import os

base_dir = Path('/tensorfl_vision/deeplearning-app')
sys.path.append(str(base_dir))

from server_flask.model_inference import InferenceEmotions
from server_flask.preprocessing.bert_preprocess import DataPreprocessing

class BertDQN(nn.Module):
    # h1 nodel container observation space
    def __init__(self, bert_output_size, h1_nodes, out_actions):
        super().__init__()
        self.fc1 = nn.Linear(bert_output_size, h1_nodes)
        self.out = nn.Linear(h1_nodes, out_actions)
        
        
    def forward(self,x):
        
        x  = F.relu(self.fc1(x))
        x = self.out(x)
        
        return x
    
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

    

# Define memory for Experience Replay
class ReplayMemory():
    def __init__(self, maxlen):
        self.memory = deque([], maxlen=maxlen)

    def append(self, transition):
        self.memory.append(transition)

    def sample(self, sample_size):
        return random.sample(self.memory, sample_size)

    def __len__(self):
        return len(self.memory)

class EmotionDetectionDQL():
    
    def __init__(self, bert_output_size, h1_nodes, learning_rate=0.001, gamma=0.9):
        self.memory = ReplayMemory(100)
        
        self.updated_model = base_dir / 'updated_model'
        
        # create policy based online networjk
        self.online_network = BertDQN(bert_output_size, h1_nodes, 2)
        self.target_network = BertDQN(bert_output_size, h1_nodes, 2 )
        
        self.target_network.load_state_dict(self.online_network.state_dict())
        
        # target networ kwill not be trained
        self.target_network.eval() # This network will not be trained
        
        # adam
        self.optimizer = optim.Adam(self.online_network.parameters(), lr=learning_rate)
        
        self.cleaning_text = DataPreprocessing()
        self.criterion = nn.MSELoss()
        
        
        self.gamma = gamma
        
        try:
            self.inference_model = InferenceEmotions()
            print(f"^^^^ Model is initialized successfullyy...^^^^")
        except Exception as e:
            
            print(f"Model Initialized is failed... Try again")
    
        # WE HAVE TO ACTIONS TO ELABORATE 
        # CORRECT OR WRONG PREDICTION    
        self.num_actions = 2

    # EPSILON POLICY
    def select_action(self, state, epsilon=0.1):
        sample = random.random()
        if sample > epsilon:
            with torch.no_grad():
                return self.online_network(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.num_actions)]], dtype=torch.long)
        
    def optimize_model(self, batch_size):
        
        if (len(self.memory)) < batch_size:
            return 0
        
        transitions = self.memory.sample(batch_size)       
        batch = Transition(*zip(*transitions))  
        
        #non_final_mask = torch.tensor(tuple(map(lambda s : s is not None, batch.next_state)), dtype=torch.bool)
        #non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
        
        
        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)
        
        # Q(s,a) generated
        state_action_values = self.online_network(state_batch).gather(1, action_batch)
        
        # prediction for next states
        next_state_values = torch.zeros(batch_size)
        
        '''
        if non_final_mask.sum() > 0:
            non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])
            next_state_values[non_final_mask] = self.target_network(non_final_next_states).max[1][0].detach()
        '''
        
        #expected_state_action_values = (next_state_values * self.gamma) + reward_batch
        expected_state_action_values = reward_batch
        #print(f"Expected state {expected_state_action_values}") 
        #loss = self.criterion(state_action_values, expected_state_action_values)
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
        #print(f"Initial state {state_action_values}") 
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item()
  
    
    def train(self, episodes, batch_size,  update_target_every, csv_file):
        data = pd.read_csv(csv_file)
        
        for episode in range(episodes):
           
            total_loss = 0
            
            
            for index, row in data.iterrows():
                cleaned_text = self.cleaning_text.preprocessingText(row['original_text'])
                state_embeddings = self.inference_model.get_embeddedings(cleaned_text)
                
                state = state_embeddings
            
                action = self.select_action(state) # implement this
                reward = torch.tensor([[1 if row['predicted_emotion'] == row['use_defined_emotion'] else -1]], dtype=torch.float)
                next_state = None  # There's no next state in this training environment
                # each example is considered as termianl state
               
            
                self.memory.append((state, action, next_state, reward))
                
                loss = self.optimize_model(batch_size)
                
                total_loss += loss
                
            if episode % update_target_every == 0:
                self.target_network.load_state_dict(self.online_network.state_dict())
                
            print(f"Episode {episode}, Loss {total_loss / index + 1}")
            
    def save_updated_model(self):
        
        try:
            if not os.path.exists(self.updated_model):
                os.makedirs(self.updated_model, exist_ok=True)
                
            model_path = os.path.join(self.updated_model, 'updated_bert.pt')
            
            torch.save(self.online_network.state_dict(), model_path)
            print('Model Saved successfully')
        except Exception as e:
            print(f'Model Saved is failed...{e}')
        
def main():
    
    
    # Example initialization and training call
    dql = EmotionDetectionDQL(bert_output_size=13, h1_nodes=256, learning_rate=0.0001, gamma=0.9)
    dql.train(episodes=30, batch_size=1, update_target_every=1, csv_file= '/tensorfl_vision/deeplearning-app/server_flask/data/user_feedback.csv')
    
    dql.save_updated_model()
if __name__ == '__main__':
    main()