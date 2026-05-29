import pandas as pd
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

def clean_text(text):
    """Cleans the input text data."""
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub(r'[‘’“”…]', '', text)
    text = re.sub(r'\n', '', text)
    return text

def train_and_save_model():
    """Trains the model and saves it with the vectorizer."""
    print("Loading data...")
    # Assumes dataset files are in ../data/
    df_fake = pd.read_csv('../data/fake.csv')
    df_true = pd.read_csv('../data/True.csv')

    # Add labels
    df_fake["class"] = 0  # Fake news
    df_true["class"] = 1  # True news

    # Combine datasets
    df_merged = pd.concat([df_fake, df_true], ignore_index=True)
    df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)

    print("Preprocessing text...")
    # Combine title and text for features
    df_merged['text'] = df_merged['title'] + ' ' + df_merged['text']
    df_merged['text'] = df_merged['text'].apply(clean_text)

    # Define features and labels
    X = df_merged['text']
    y = df_merged['class']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    print("Vectorizing text...")
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")
    # Initialize and train the model
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    print("Evaluating model...")
    # Make predictions and evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    print("Saving model and vectorizer...")
    # Save the trained model and vectorizer
    with open('trained_model/model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

    with open('trained_model/vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)

    print("Model training complete and files saved.")

if __name__ == '__main__':
    # Create the directory if it doesn't exist
    import os
    if not os.path.exists('trained_model'):
        os.makedirs('trained_model')
    train_and_save_model()