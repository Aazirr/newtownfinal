import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
import os

@st.cache_resource
def load_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

def is_valid_suggestion(suggestion):
    return suggestion.isalnum()

def suggest_next_words(text, num_suggestions=5):
    text = text.rstrip()
    input_ids = tokenizer.encode(text, return_tensors='pt')
    if input_ids.size(1) > 1024:
        input_ids = input_ids[:, -1024:]

    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss, logits = outputs[:2]
        next_token_logits = logits[0, -1, :]
        next_token_probs = torch.softmax(next_token_logits, dim=-1)
        top_tokens = torch.topk(next_token_probs, num_suggestions * 2)

    suggestions = []
    for token in top_tokens.indices:
        word = tokenizer.decode(token.item()).strip()
        if is_valid_suggestion(word):
            suggestions.append(word)
        if len(suggestions) >= num_suggestions:
            break
    return suggestions

st.title("Next Word Suggestion App")

if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

input_text = st.text_area("Detected text:", st.session_state.input_text, height=200)

num_suggestions = st.slider("Number of suggestions:", 1, 10, 5)

if input_text:
    suggestions = suggest_next_words(input_text, num_suggestions)
    st.write("Next word suggestions:")
    for suggestion in suggestions:
        if st.button(suggestion):
            st.session_state.input_text = input_text + " " + suggestion
            st.experimental_rerun()

def check_for_file_update(file_path, last_mod_time):
    try:
        current_mod_time = os.path.getmtime(file_path)
        if current_mod_time != last_mod_time:
            with open(file_path, "r") as file:
                st.session_state.input_text = file.read()
            return current_mod_time
    except FileNotFoundError:
        pass
    return last_mod_time

if 'file_mod_time' not in st.session_state:
    st.session_state.file_mod_time = 0

st.session_state.file_mod_time = check_for_file_update("current_text.txt", st.session_state.file_mod_time)

# Schedule a rerun
time.sleep(0.5)
st.experimental_rerun()
