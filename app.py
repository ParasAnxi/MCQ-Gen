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

sample_text = read_text_file('./data/sample_text.txt')
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(pre_process_text(sample_text))
padded_sequences = build_training_data(sample_text, tokenizer = tokenizer,max_length = 20)

# print(padded_sequences)

# @app.route('/', methods = ["GET", "POST"])
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 3000))
#     app.run(host='0.0.0.0', port = port, debug = True)