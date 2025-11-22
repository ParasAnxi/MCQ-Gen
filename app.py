from flask import Flask, render_template, request, send_file, session, url_for, redirect
from flask_bootstrap import Bootstrap
import spacy
import random
from collections import Counter
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

app = Flask(__name__)
app.secret_key = "afskj988fdhafh893hkajsfjkhsf"
Bootstrap(app)

nlp = spacy.load("en_core_web_md")

def read_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def pre_process_text(text):
    document = nlp(text)
    sentences = [sentence.text for sentence in document.sents]
    return sentences

def build_training_data(text, tokenizer, max_length):
    sentences = pre_process_text(text)
    sequences = tokenizer.texts_to_sequences(sentences)
    padded_sequences = pad_sequences(sequences, maxlen = max_length, padding = "post")
    return padded_sequences   

def build_lstm_model(vocabulary_size, max_length, embedding_dimension):
    model = Sequential([
        Embedding(vocabulary_size , embedding_dimension, input_length = max_length),
        LSTM(128 , return_sequences = True),
        Dropout(0.2),
        LSTM(64),
        Dense(64, activation = "relu"),
        Dense(vocabulary_size, activation = "softmax")
    ])
    model.compile(loss='sparse_categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
    return model


def find_similar_words(word, similar_num = 3):
    word_token = nlp(word)[0]
    if not word_token.has_vector:
        return ["[Distractor]"] * similar_num

    similarities = []
    for token in nlp.vocab:
        if token.is_alpha and token.has_vector and token.text.lower() != word.lower():
            similarity = word_token.similarity(token)
            similarities.append((token.text, similarity))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return [w for w, sim in similarities[:similar_num]]


def generate_mcqs(text, tokenizer, max_length, model, n_ques = 5):
    sentences = pre_process_text(text)
    if not sentences:
        return []

    selected_sentences = random.sample(sentences, min(n_ques, len(sentences)))
    mcqs = []
    for sentence in selected_sentences:
        doc = nlp(sentence)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        if len(nouns) < 1:
            continue
        subject = random.choice(nouns)
        question_stem = sentence.replace(subject, "______")
        similar_words = find_similar_words(subject, similar_num = 3)
        answer_choices = [subject] + similar_words
        random.shuffle(answer_choices)
        correct_answer = chr(65 + answer_choices.index(subject))
        mcqs.append((question_stem, answer_choices, correct_answer))
    return mcqs

sample_text = read_text_file('./data/sample_text.txt')
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(pre_process_text(sample_text))
padded_sequences = build_training_data(sample_text, tokenizer = tokenizer,max_length = 20)
vocabulary_size = len(tokenizer.word_index) + 1
max_length = 20
model = build_lstm_model(vocabulary_size, max_length, embedding_dimension = 100)

print(generate_mcqs(sample_text, tokenizer, max_length, model))

# @app.route('/', methods = ["GET", "POST"])
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 3000))
#     app.run(host='0.0.0.0', port = port, debug = True)