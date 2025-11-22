import spacy
import random
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

nlp = spacy.load("en_core_web_md")

def preprocess_text(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def create_training_data(sentences, tokenizer, max_length):
    sequences = tokenizer.texts_to_sequences(sentences)
    return pad_sequences(sequences, maxlen=max_length, padding="post")


def build_lstm_model(vocab_size, max_length, embedding_dim):
    model = Sequential([
        Embedding(vocab_size, embedding_dim, input_length=max_length),
        LSTM(128, return_sequences=True),
        Dropout(0.2),
        LSTM(64),
        Dense(64, activation="relu"),
        Dense(vocab_size, activation="softmax")
    ])
    model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model


def find_similar_words(word, num_similar=3):
    word_token = nlp(word)[0]
    if not word_token.has_vector:
        return ["[Distractor]"] * num_similar
    similarities = [
        (token.text, word_token.similarity(token))
        for token in nlp.vocab
        if token.is_alpha and token.has_vector and token.text.lower() != word.lower()
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [w for w, _ in similarities[:num_similar]]


def generate_mcqs(text, tokenizer, max_length, model, num_questions=5):
    sentences = preprocess_text(text)
    if not sentences:
        return []

    selected_sentences = random.sample(
        sentences, min(num_questions + 1, len(sentences)))
    mcqs = []
    for sentence in selected_sentences:
        doc = nlp(sentence)
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        if not nouns:
            continue

        subject = random.choice(nouns)
        question_stem = sentence.replace(subject, "______")
        similar_words = find_similar_words(subject, num_similar=3)
        answer_choices = [subject] + similar_words
        random.shuffle(answer_choices)
        correct_answer = chr(65 + answer_choices.index(subject))

        mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs
