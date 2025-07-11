import joblib
clf = joblib.load("itmo_model.pkl")
def predict_from_input(query, title, cpu, ram, storage, gpu):
    row = {
        "query": query,
        "title": title,
        "cpu": cpu,
        "ram": ram,
        "storage": storage,
        "gpu": gpu
    }
    feats = extract_features(row)
    pred = clf.predict([feats])[0]
    return label_rev_map[pred]
#print(predict_from_input(
    "ноутбук для видео",
    "ASUS VivoBook",
    "Ryzen 3 3500U",
    "8 GB RAM",
    "512 GB SSD",
    "встроенная графика"
))#для вывода результата: print(predict_from_input('текст'))
