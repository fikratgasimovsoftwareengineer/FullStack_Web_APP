# Architecture
It is a language model that utilizes a transformer based architecture and comprises of several key components like Input Embeddings, Encoder layers, Decoder layers and Output Layers.

Input Embedding : In this the input text is converted to numerical representations that can be understood by the model. The embedding layer is being deployed for this task which maps each word or token in the input seq to a high dim vector.
Encoder layer - GPT2 consists of multiple identical encoder layers stacked over each other. Each encoder layer has two sub layers which are a self attention mechanism and feed forwd network. The self attention mechanism allows the model to weigh the importance of diff words or tokens with inp. seq thereby capturing the dependencies and relationships betw. them. The feed forward network processes the self attn outputs to gen more complex representations.
Decoder layer - It follows the encoder layers and has a similar structure as it also consists of self attention and feed forward layers. Just that in this the decoder layer is conditioned on the context from the prev. tokens enabling autoregressive generation. This means the model predicts the next word in the seq based on the context it has learned so far.
Output layer - The final layer of GPT2 is a linear transformation followed by a softmax activation function. This layer produces the prob. distribution over the vocab for the next word in the sequence. It alows the model to generate text by sampling from the distribution or choosing the word with the highest probability.

## NOTE:

Please download dataset from the hugging face as mentioned in the link : (medium articles)[https://huggingface.co/datasets/fabiochiu/medium-articles]
