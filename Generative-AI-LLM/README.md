# Generative AI with LLMs TUTORIAL
In Generative AI with Large Language Models (LLMs), you’ll learn the fundamentals of how generative AI works, and how to deploy it in real-world applications.

By taking this course, you'll learn to:

- Deeply understand generative AI, describing the key steps in a typical LLM-based generative AI lifecycle, from data gathering and model selection, to performance evaluation and deployment
- Describe in detail the transformer architecture that powers LLMs, how they’re trained, and how fine-tuning enables LLMs to be adapted to a variety of specific use cases
- Use empirical scaling laws to optimize the model's objective function across dataset size, compute budget, and inference requirements
Apply state-of-the art training, tuning, inference, tools, and deployment methods to maximize the performance of models within the specific constraints of your project
- Discuss the challenges and opportunities that generative AI creates for businesses after hearing stories from industry researchers and practitioners

Developers who have a good foundational understanding of how LLMs work, as well the best practices behind training and deploying them, will be able to make good decisions for their companies and more quickly build working prototypes. This course will support learners in building practical intuition about how to best utilize this exciting new technology.

## SESSION ONE
Generative AI use cases, project lifecycle, and model pre-training

#### Learning Objectives

- Discuss model pre-training and the value of continued pre-training vs fine-tuning
- Define the terms Generative AI, large language models, prompt, and describe the transformer architecture that powers LLMs
- Describe the steps in a typical LLM-based, generative AI model lifecycle and discuss the constraining factors that drive decisions at each step of model lifecycle
- Discuss computational challenges during model pre-training and determine how to efficiently reduce memory footprint
- Define the term scaling law and describe the laws that have been discovered for LLMs related to training dataset size, compute budget, inference requirements, and other factors
- Deep Explanation of Zero Shot, One Shot and Few Shot Inference with Prompt Engineering
- Use Cases of Zero Shot, Few SHot and Few Shot Inference together with LLM



# Useful Scientific Resources

Below you'll find links to the research papers discussed in throughout videos. You don't need to understand all the technical details discussed in these papers - you have already seen the most important points you'll need to answer the quizzes in the lecture videos. 

However, if you'd like to take a closer look at the original research, you can read the papers and articles via the links below. 


### Generative AI Lifecycle
Generative AI on AWS: Building Context-Aware, Multimodal Reasoning Applications
 - (This O'Reilly book dives deep into all phases of the generative AI lifecycle including model selection, fine-tuning, adapting, evaluation, deployment, and runtime optimizations)[https://www.amazon.com/Generative-AI-AWS-Multimodal-Applications/dp/1098159225/]
Transformer Architecture
### Attention is All You Need
 - (This paper introduced the Transformer architecture, with the core “self-attention” mechanism. This article was the foundation for LLMs)[https://arxiv.org/pdf/1706.03762]

BLOOM: BigScience 176B Model 
 - (BLOOM is a open-source LLM with 176B parameters trained in an open and transparent way. In this paper, the authors present a detailed discussion of the dataset and process used to train the model. You can also see a high-level overview of the model) [https://arxiv.org/abs/2211.05100]
here
.

(Vector Space Models)[https://www.coursera.org/learn/classification-vector-spaces-in-nlp/home/week/3]
 - Series of lessons from DeepLearning.AI's Natural Language Processing specialization discussing the basics of vector space models and their use in language modeling.

### Pre-training and scaling laws
Scaling Laws for Neural Language Models[https://arxiv.org/abs/2001.08361]
 - empirical study by researchers at OpenAI exploring the scaling laws for large language models.

### Model architectures and pre-training objectives
What Language Model Architecture and Pretraining Objective Work Best for Zero-Shot Generalization?
 - (The paper examines modeling choices in large pre-trained language models and identifies the optimal approach for zero-shot generalization.)[https://arxiv.org/pdf/2204.05832.pdf]

HuggingFace Tasks [https://huggingface.co/tasks]
 and 
Model Hub[https://huggingface.co/models]
 - Collection of resources to tackle varying machine learning tasks using the HuggingFace library.

LLaMA: Open and Efficient Foundation Language Models[https://arxiv.org/pdf/2302.13971.pdf]
 - Article from Meta AI proposing Efficient LLMs (their model with 13B parameters outperform GPT3 with 175B parameters on most benchmarks)

### Scaling laws and compute-optimal models
Language Models are Few-Shot Learners
 - This paper investigates the potential of few-shot learning in Large Language Models.[https://arxiv.org/pdf/2005.14165.pdf]

Training Compute-Optimal Large Language Models
 - Study from DeepMind to evaluate the optimal model size and number of tokens for training LLMs. Also known as “Chinchilla Paper”.[https://arxiv.org/pdf/2203.15556.pdf]

BloombergGPT: A Large Language Model for Finance
 - LLM trained specifically for the finance domain, a good example that tried to follow chinchilla laws.[https://arxiv.org/pdf/2303.17564.pdf]


## SECOND SESSION

#### Learning Objectives
- Describe how fine-tuning with instructions using prompt datasets can improve performance on one or more tasks
- Define catastrophic forgetting and explain techniques that can be used to overcome it
- Define the term Parameter-efficient Fine Tuning (PEFT)
- Explain how PEFT decreases computational cost and overcomes catastrophic forgetting
- Explain how fine-tuning with instructions using prompt datasets can increase LLM performance on one or more

## THIRD SESSION

#### Learning Objectives

- Describe how RLHF uses human feedback to improve the performance and alignment of large language models
- Explain how data gathered from human labelers is used to train a reward model for RLHF
- Define chain-of-thought prompting and describe how it can be used to improve LLMs reasoning and planning abilities
- Discuss the challenges that LLMs face with knowledge cut-offs, and explain how information retrieval and augmentation techniques can overcome these challenges






