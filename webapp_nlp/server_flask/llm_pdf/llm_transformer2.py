import fitz  # PyMuPDF for PDF processing
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

class ContentAnalyzer2:
    def __init__(self):
        # Initialize tokenizer and model for question answering
        self.tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
        self.max_length = 512
        self.stride = 128
        self.chunks = []  # Initialize chunks as an empty list
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        self.model.to(self.device)

    def extract_text_from_pdf(self, pdf_path):
        # Open PDF and extract text
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        self.split_into_chunks(text)  # Split the text into manageable chunks

    def split_into_chunks(self, context):
        # Tokenize the context and create chunks
        tokens = self.tokenizer(context, truncation=True, max_length=self.max_length, return_overflowing_tokens=True, stride=self.stride, return_offsets_mapping=True)
        for token_set in tokens.encodings:
            self.chunks.append(self.tokenizer.decode(token_set.ids))

    def find_best_answer(self, question):
        max_score = -float('inf')  # Initialize max score to negative infinity
        best_answer = "Sorry, I couldn't find an answer."  # Default answer

        
        for chunk in self.chunks:
            
            inputs = self.tokenizer.encode_plus(question, chunk, return_tensors="pt", truncation=True)
            
            # move tensor to same device
            inputs = { k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.model(**inputs)

            # move your result back to cpu
            answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits

            answer_start = torch.argmax(answer_start_scores).item()
            answer_end = torch.argmax(answer_end_scores).item() + 1

            score = answer_start_scores[0, answer_start].cpu().item() + answer_end_scores[0, answer_end - 1].cpu().item()

            if score > max_score:
                max_score = score
                best_answer = self.tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end].cpu().tolist(), skip_special_tokens=True)

        return best_answer
