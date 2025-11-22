import spacy
from tensorflow.keras.preprocessing.text import Tokenizer
from .nlp_utils import preprocess_text, build_lstm_model

nlp = spacy.load("en_core_web_md")

# Sample text for tokenizer training
sample_text = """Deep learning is a subset of machine learning that uses neural networks. 
LSTMs are useful for processing sequential data like text. 
Natural language processing involves tokenization and named entity recognition."""
sentences = preprocess_text(sample_text)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
vocab_size = len(tokenizer.word_index) + 1
max_length = 20

model = build_lstm_model(vocab_size, max_length, embedding_dim=100)
