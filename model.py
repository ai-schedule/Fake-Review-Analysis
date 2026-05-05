from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np

# ---------------- TRAIN + SAVE ----------------
def train_model(df):

    tfidf = TfidfVectorizer(max_features=7000, ngram_range=(1,2))
    X = tfidf.fit_transform(df['clean_text'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearSVC(max_iter=2000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    # Save model
    joblib.dump(model, "model.pkl")
    joblib.dump(tfidf, "tfidf.pkl")

    return model, tfidf, accuracy, report


# ---------------- LOAD MODEL ----------------
def load_model():
    model = joblib.load("model.pkl")
    tfidf = joblib.load("tfidf.pkl")
    return model, tfidf


# ---------------- ANALYSIS ----------------
def analyze_multiple_reviews(model, tfidf, reviews, clean_function):
    fake_count = 0

    for review in reviews:
        clean = clean_function(review)
        vector = tfidf.transform([clean])
        pred = model.predict(vector)[0]

        if pred == 1:
            fake_count += 1

    total = len(reviews)
    fake_percentage = (fake_count / total) * 100
    trust_score = 100 - (fake_percentage )

    return trust_score, fake_percentage


# ---------------- EXPLANATION ----------------
def generate_explanation(fake_percentage):
    reasons = []

    if fake_percentage >= 60:
        reasons.append("Very high number of suspicious reviews detected")
        reasons.append("Product appears highly unreliable")

    elif fake_percentage >= 40:
        reasons.append("Significant number of suspicious reviews found")
        reasons.append("Possible manipulation in reviews")

    elif fake_percentage >= 20:
        reasons.append("Some reviews may be fake")
        reasons.append("Product shows moderate trust")

    else:
        reasons.append("Most reviews appear genuine")
        reasons.append("Product looks trustworthy")

    return reasons
