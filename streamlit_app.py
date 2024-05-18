import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

@st.cache_resource
def load_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

def suggest_next_words(text, num_suggestions=5):
    input_ids = tokenizer.encode(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss, logits = outputs[:2]
        next_token_logits = logits[0, -1, :]
        next_token_probs = torch.softmax(next_token_logits, dim=-1)
        top_tokens = torch.topk(next_token_probs, num_suggestions)
    
    suggestions = []
    for token in top_tokens.indices:
        word = tokenizer.decode(token.item())
        suggestions.append(word.strip())
    return suggestions

st.title("Next Word Suggestion App")
st.write("Type a sentence and get next word suggestions!")

user_input = st.text_input("Enter your text here:", "")
num_suggestions = st.slider("Number of suggestions:", 1, 10, 5)

if user_input:
    suggestions = suggest_next_words(user_input, num_suggestions)
    st.write("Next word suggestions:")
    for suggestion in suggestions:
        st.write(f"- {suggestion}")
