import json
import requests
from fastapi import FastAPI, Body
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

IAM_TOKEN = 't1.9euelZrKm5iYzZ7GlMzLzJuOnM6Jy-3rnpWam4uXnZyci8uRi5iQzczNyMvl8_dXTxle-e86DSBc_N3z9xd-Fl757zoNIFz8.g_5BsMdFkbbhVnpMmqgRsk8BYsyriYFjmcpQoIqsXWgcqFySvcgCsxp4rfBQKcm5YefoRwGREdn9mlmz8oNcDw'
folder_id = 'b1gq88cm7pq2tr39ka4r'
target_language = 'ru'
texts = []

body = {
    "targetLanguageCode": target_language,
    "texts": texts,
    "folderId": folder_id,
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/gettrans")
def transResponse(data=Body()):
    ...

@app.post("/api/totrans")
def transRequest(data=Body()):
    texts.append(data["word"])
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    texts.pop(0)
    dict_response = json.loads(response.text)
    data["word"] = dict_response['translations'][0]['text']
    print(data["word"])
    return data

@app.post("/api/totag")
def tagRequest(data=Body()):
    print(data["tag_word"])
    print(data["email_word"])
    return data

if __name__ == '__main__':
    uvicorn.run(app='server:app', reload=True)

