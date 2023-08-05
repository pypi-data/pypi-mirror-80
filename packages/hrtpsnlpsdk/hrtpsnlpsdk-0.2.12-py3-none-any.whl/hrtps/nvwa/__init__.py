import requests
from tqdm import tqdm


class NvwaPredict(object):

    def __init__(self, host, port, endpoint):
        self.host = host
        self.port = port
        self.endpoint = endpoint

        self.dim_name = {
            "1": "AchievementOriented",
            "2": "Innovation",
            "3": "LearningAbility",
            "4": "Resilience",
            "5": "Execution",
            "6": "TeamWork",
        }

    def predict(self, doc_text, model_type: int):
        purl = f"http://{self.host}:{self.port}/{self.endpoint}"
        pdata = {
            "params": {
                "docText": doc_text,
                "model_type": model_type
            }
        }
        header = {
            "Content-Type": "application/json",
            "Auth": "dc5976de",
        }
        resp = requests.post(purl, json=pdata, headers=header)
        return resp.json()["result"]

    def predict_all(self, doc_text):
        pre_result = {}

        for i in range(1, 7):
            pre_score = self.predict(doc_text, i)
            pre_result[str(i)] = pre_score * 0.01
        return pre_result


class SimPredict(object):

    def __init__(self, host, port, endpoint, auth):
        self.host = host
        self.port = port
        self.endpoint = endpoint
        self.auth = auth

    def predict(self, doc, sta):
        purl = f"http://{self.host}:{self.port}/{self.endpoint}"
        pdata = {
            "params": {
                "docText": doc,
                "template": sta
            }
        }
        header = {
            "Content-Type": "application/json",
            "Auth": self.auth,
        }
        resp = requests.post(purl, json=pdata, headers=header)
        return resp.json()["result"]

    def predict_all(self, docs, stas):
        pre_result = []

        for i, doc in enumerate(docs):
            sta = stas[i]
            pre_score = self.predict(doc, sta)
            pre_result.append(pre_score * 0.01)
        return pre_result

