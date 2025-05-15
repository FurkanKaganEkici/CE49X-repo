
import pandas as pd
import numpy as np
import json
import os
import re
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from scipy.sparse import hstack
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(file_name):
    path = os.path.join(os.path.dirname(__file__), file_name)
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return pd.DataFrame(data)


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def preprocess_metadata(df):
    imp = SimpleImputer(strategy='most_frequent')
    df[['project_phase', 'author_role']] = imp.fit_transform(df[['project_phase', 'author_role']])
    metadata = df[['project_phase', 'author_role']].to_dict(orient='records')
    dv = DictVectorizer(sparse=False)
    return dv.fit_transform(metadata), dv


def vectorize_text(df, method='tfidf'):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500) if method == 'tfidf' else CountVectorizer(stop_words='english', max_features=500)
    X_text = vectorizer.fit_transform(df['clean_content'])
    return X_text, vectorizer


def train_and_evaluate(X_train, X_test, y_train, y_test):
    model = MultinomialNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    return model, y_pred


def plot_confusion(y_test, y_pred, labels):
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()


def analyze_misclassifications(y_test, y_pred):
    errors = (y_test != y_pred)
    if errors.any():
        print("\nSample Misclassifications:")
        print(y_test[errors].head())
    else:
        print("\nNo misclassifications. Model predictions are perfect.")


def show_top_keywords(vectorizer, model, labels, metadata_size):
    feature_names = vectorizer.get_feature_names_out()
    for i, label in enumerate(labels):
        text_log_probs = model.feature_log_prob_[i][metadata_size:]
        top10 = np.argsort(text_log_probs)[-5:][::-1]
        print(f"{label}: {', '.join(feature_names[top10])}")


def main():
    construction_documents = os.path.join(os.path.dirname(__file__), "..", "..", "datasets", "construction_documents.json")
    df = load_data(construction_documents)
    df['clean_content'] = df['content'].apply(preprocess_text)
    metadata_features, dv = preprocess_metadata(df)

    for method in ['count', 'tfidf']:
        print(f"\n================= Using {method.upper()} Vectorizer =================")
        text_features, vectorizer = vectorize_text(df, method=method)
        metadata_sparse = np.array(metadata_features)
        X_combined = hstack([metadata_sparse, text_features])
        y = df['document_type']

        X_train, X_test, y_train, y_test = train_test_split(
            X_combined, y, test_size=0.2, random_state=42, stratify=y)

        model, y_pred = train_and_evaluate(X_train, X_test, y_train, y_test)
        labels = model.classes_
        plot_confusion(y_test, y_pred, labels)
        analyze_misclassifications(y_test.reset_index(drop=True), pd.Series(y_pred))
        print("\nTop keywords per class:")
        show_top_keywords(vectorizer, model, labels, metadata_features.shape[1])
        scores = cross_val_score(MultinomialNB(), X_combined, y, cv=5, scoring='accuracy')
        print(f"Cross-Validation Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")


if __name__ == "__main__":
    main()
