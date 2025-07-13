import joblib
model = joblib.load("rf_genre_model.joblib")
vectorizer = joblib.load("tfidf_vectorizer_genre.joblib")
def predict_genre(text):
    vec = joblib.load('tfidf_vectorizer_genre.joblib')
    model = joblib.load('rf_genre_model.joblib')
    text_vec = vec.transform([text])
    pred = model.predict(text_vec)
    return pred[0]
#------------
print(predict_genre(""))
