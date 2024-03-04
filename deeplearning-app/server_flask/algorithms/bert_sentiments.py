from transformers import BertModel
import torch
import torch.nn as nn
import os


class BertClassSentimentsLast(nn.Module):

    def __init__(self):
        super(BertClassSentimentsLast, self).__init__()

        self.layer_bert = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True, hidden_dropout_prob=0.5)

        # Freeze all layers except the last two
        for name, param in self.layer_bert.named_parameters():
            if 'layer8' not in name and 'layer9' not in name and 'layer.10' not in name and 'layer.11' not in name:  # last two layers are 10 and 11 for BERT base
                param.requires_grad = False

        self.dense = nn.Linear(768*4, 256)
        self.norm1 = nn.BatchNorm1d(256)
        self.relu = nn.ReLU()
        self.final = nn.Linear(256, 13)
        self.norm2 = nn.BatchNorm1d(13)

    def forward(self, input_ids, mask):
        outputs = self.layer_bert(input_ids, attention_mask=mask, return_dict=True)
        hidden_states = outputs.hidden_states
        last_hidden_states = torch.cat((hidden_states[-1], hidden_states[-2], hidden_states[-3], hidden_states[-4]), dim=-1)

        # global max pooling
        pooled_output = torch.max(last_hidden_states, dim=1).values

        # add to dense
        x = self.dense(pooled_output)
        x = self.norm1(x)
        x = self.relu(x)
        x = self.final(x)
        x = self.norm2(x)

        return x


    def save_entire_model(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        model_path = os.path.join(output_dir, "finetuned_model.pt")
        torch.save(self.state_dict(), model_path)