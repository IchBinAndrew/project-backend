import joblib
model = joblib.load("logic_classifier_rf.joblib")
vectorizer = joblib.load("logic_vectorizer.joblib")

def predict_relation(first_fact, second_fact):
    text = first_fact + " [SEP] " + second_fact
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return prediction
#--------
print(predict_relation(
    "ел раков",
    "выпал снег"))
