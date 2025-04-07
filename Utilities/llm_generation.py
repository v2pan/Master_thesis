import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import json
from huggingface_hub import login


# Your provided constants
def read_hf_token(file_path='token.txt'):
    with open(file_path, 'r') as file:
        token = file.readline().strip()  # Read and strip any surrounding whitespace
    return token

# Use the token
HF_TOKEN = read_hf_token('token.txt')

LLM_MODEL_NAME = "meta-llama/Llama-3.2-3B"

class TextLLM:
    def __init__(self, model_name=LLM_MODEL_NAME):
        login(HF_TOKEN)
        # Load the tokenizer and model from Hugging Face
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Optionally, we can set the device to GPU if it's available, else CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

        # Set up the Hugging Face pipeline for text generation
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0 if self.device == "cuda" else -1)

    def __call__(self, prompt, boolean=False, instruction_prompt="", return_metadata=False):
      full_prompt = f"{instruction_prompt}\n{prompt}"

      generated_text = None
      prompt_tok = None
      answer_tok = None

      if not boolean:
          # Normal generation
          prompt_tok = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
          output = self.generator(full_prompt, max_length=512, num_return_sequences=1)
          generated_text = output[0]['generated_text']
          answer_tok = self.tokenizer(generated_text, return_tensors="pt").to(self.device)
      else:
          # Force Yes/No answer
          full_prompt = f"Answer the following questions with only Yes or No.\n{full_prompt}"
          max_attempts = 5
          attempt = 0
          generated_answer = None

          while generated_answer not in [True, False] and attempt < max_attempts:
              prompt_tok = self.tokenizer(full_prompt, return_tensors="pt").to(self.device)
              output = self.generator(full_prompt, max_length=512, num_return_sequences=1)
              generated_text = output[0]['generated_text']
              answer_tok = self.tokenizer(generated_text, return_tensors="pt").to(self.device)

              # Determine if the model said yes or no
              if "yes " in generated_text.lower():
                  generated_answer = True
              elif "no " in generated_text.lower():
                  generated_answer = False
              else:
                  generated_answer = None
                  attempt += 1

          generated_text = generated_answer  # Will be True/False or None if all attempts failed

      # Prepare metadata
      metadata = None
      if return_metadata and prompt_tok is not None and answer_tok is not None:
          metadata = {
              "prompt_token_count": prompt_tok['input_ids'].shape[1],
              "candidates_token_count": answer_tok['input_ids'].shape[1] - prompt_tok['input_ids'].shape[1],
              "total_token_count": answer_tok['input_ids'].shape[1],
              "total_calls": attempt + 1 if boolean else 1
          }

      return generated_text, metadata

    def get_embedding(self, text, pooling: str = "mean"):
      """
      Generate an embedding from the model's hidden states using the tokenizer and model.

      :param text: The input string.
      :param pooling: Pooling method - "mean", "cls", or "last".
      :return: embedding tensor
      """
      inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
      with torch.no_grad():
          outputs = self.model(**inputs, output_hidden_states=True)
          hidden_states = outputs.hidden_states[-1]  # Last layer: [batch_size, seq_len, hidden_dim]

      if pooling == "mean":
          # Average pooling across token dimension (excluding padding)
          attention_mask = inputs['attention_mask'].unsqueeze(-1)
          sum_hidden = (hidden_states * attention_mask).sum(dim=1)
          count_nonzero = attention_mask.sum(dim=1)
          embedding = sum_hidden / count_nonzero
      elif pooling == "cls":
          # Use first token (often not trained like CLS, but okay)
          embedding = hidden_states[:, 0, :]
      elif pooling == "last":
          # Use last token's hidden state
          input_lengths = inputs['attention_mask'].sum(dim=1) - 1
          embedding = hidden_states[torch.arange(hidden_states.size(0)), input_lengths]
      else:
          raise ValueError("Invalid pooling type. Choose from 'mean', 'cls', or 'last'.")

      return embedding.squeeze(0).cpu()
  