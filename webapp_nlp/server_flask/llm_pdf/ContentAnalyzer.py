import fitz  # PyMuPDF
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to split the text into chunks that fit the model's maximum input size
def split_into_chunks(context, tokenizer, max_length=512, stride=50):
    # Tokenize the context and create chunks
    '''What are attention masks?

return_overflowing_tokens (bool, optional, defaults to False) — Whether or not to return overflowing token sequences.
 If a pair of sequences of input ids (or a batch of pairs) is provided with truncation_strategy
 = longest_first or True, an error is raised instead of returning overflowing tokens.
    '''
    tokens = tokenizer(context, truncation=True, max_length=max_length, return_overflowing_tokens=True, stride=stride, return_offsets_mapping=True)
    chunk_mapping = tokens.pop("overflow_to_sample_mapping")
    chunks = [tokenizer.decode(tokens["input_ids"][i]) for i in range(len(chunk_mapping))]
    return chunks

# Function to find the best answer from the chunks
def find_best_answer(question, chunks, tokenizer, model):
    max_score = None
    best_answer = ""
    for chunk in chunks:
        inputs = tokenizer.encode_plus(question, chunk, add_special_tokens=True, return_tensors="pt", truncation=True)
        input_ids = inputs["input_ids"].tolist()[0]
        outputs = model(**inputs)
        answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits

        # Find the best answer for this chunk
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1
        score = torch.max(answer_start_scores) + torch.max(answer_end_scores)

        if max_score is None or score > max_score:
            max_score = score
            answer_tokens = input_ids[answer_start:answer_end]
            best_answer = tokenizer.decode(answer_tokens, skip_special_tokens=True)

    return best_answer

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

# Example usage
# Example usage
# Example usage
pdf_path = "/tensorfl_vision/QuestionAnswering/input/D_Strange-Girl_Meets_Boy_Penguin_Readers-1-min.pdf"
context = extract_text_from_pdf(pdf_path)

# Split the context into chunks
chunks = split_into_chunks(context, tokenizer)


# List of questions to ask
questions = [
    "How do they travel to Spain?",
    "Which services did the boat have inside it?",
    "At what time did they arrive in Santander?"
]

print('--------INFERENCE--------------------')
# Iterate through each question and find the best answer
for question in questions:
    answer = find_best_answer(question, chunks, tokenizer, model)
    print(f"Question: {question}\nAnswer: {answer}\n")


