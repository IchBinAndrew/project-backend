import joblib
import enum
import re
clf = joblib.load("itmo_model.pkl")

class CategoryEnum(enum.Enum):
    CONTENT = 1
    GAMING = 2
    WORK = 3

class ModelEnum(str, enum.Enum):
    INTEL = "Intel"
    AMD = "AMD"


def extract_features(row):
    data = [
        row["query"],
        row["title"],
        row["cpu"],
        row["ram"],
        row["storage"],
        row["gpu"]
    ]

    task_keywords = {
        "видео": CategoryEnum.CONTENT,
        "игр": CategoryEnum.GAMING,
        "работ": CategoryEnum.WORK
    }
    task_class = 0
    for k, v in task_keywords.items():
        if k in data[0].lower():
            task_class = v.value
            break

    cpu_text = data[2].lower()
    cpu_brand = 1 if "intel" in cpu_text else 2 if "ryzen" in cpu_text or "amd" in cpu_text else 0
    cpu_gen = 0
    try:
        cpu_gen = int(re.findall(r"\d{4,5}", cpu_text)[0])
    except Exception:
        pass

    cpu_perf = cpu_performance_score(cpu_text)

    ram_num = 0
    try:
        ram_num = int(re.findall(r"\d+", data[3])[0])
    except Exception:
        pass

    storage_num = 0
    try:
        storage_num = int(re.findall(r"\d+", data[4])[0])
    except Exception:
        pass

    gpu_power = gpu_performance_score(data[5].lower())

    return [task_class, cpu_brand, cpu_gen, cpu_perf, ram_num, storage_num, gpu_power]

def cpu_performance_score(cpu_text: str) -> int:
    cpu_text = cpu_text.lower()
    score = 0
    if "apple m" in cpu_text:
        if "max" in cpu_text:
            score = 10
        elif "pro" in cpu_text:
            score = 9
        else:
            score = 8
    elif "intel" in cpu_text:
        if "i9" in cpu_text:
            score = 9
        elif "i7" in cpu_text:
            score = 7
        elif "i5" in cpu_text:
            score = 5
        elif "i3" in cpu_text:
            score = 3
        elif "xeon" in cpu_text:
            score = 8
        else:
            score = 2
    elif "ryzen" in cpu_text or "amd" in cpu_text:
        if "9" in cpu_text:
            score = 9
        elif "7" in cpu_text:
            score = 7
        elif "5" in cpu_text:
            score = 5
        elif "3" in cpu_text:
            score = 3
        else:
            score = 2
    else:
        score = 1
    return score

def gpu_performance_score(gpu_text: str) -> int:
    gpu_text = gpu_text.lower()
    if "rtx 4090" in gpu_text:
        return 95
    elif "rtx 4080" in gpu_text:
        return 90
    elif "rtx 4070" in gpu_text:
        return 85
    elif "rtx 4060" in gpu_text:
        return 80
    elif "rtx 3080" in gpu_text:
        return 75
    elif "rtx 3070" in gpu_text:
        return 70
    elif "rtx 3060" in gpu_text:
        return 65
    elif "rtx 3050" in gpu_text:
        return 60
    elif "gtx 1660" in gpu_text or "gtx 1650" in gpu_text:
        return 50
    elif "gtx 1050" in gpu_text:
        return 40
    elif any(x in gpu_text for x in ["iris", "uhd", "vega", "встроенная", "без дискретной", "integrated gpu", "intel hd", "intel iris"]):
        return 10
    elif gpu_text.strip() == "":
        return 0
    else:
        return 5



def predict_from_input(query, title, cpu, ram, storage, gpu):
    row = {
        "query": query,
        "title": title,
        "cpu": cpu,
        "ram": ram,
        "storage": storage,
        "gpu": gpu
    }
    label_map = {"✅": 0, "⚠️": 1, "❌": 2, "❓": 3}
    label_rev_map = {v: k for k, v in label_map.items()}
    feats = extract_features(row)
    pred = clf.predict([feats])[0]
    return label_rev_map[pred]
print(predict_from_input(
    "ноутбук для видео",
    "Acer Nitro V15",
    "Ryzen 7 8845HS",
    "16 GB RAM",
    "512 GB SSD",
    "RTX 3050"
))#для вывода результата: print(predict_from_input('текст'))
