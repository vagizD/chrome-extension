import json
import requests
from fastapi import FastAPI, Body
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

IAM_TOKEN = 't1.9euelZqcjceYl8bLlsnOipOeyMfGlu3rnpWam4uXnZyci8uRi5iQzczNyMvl8_d4Dkdf-e9GAy9p_t3z9zg9RF_570YDL2n-.c43swKOubcubP_9VVLqlTELU2Je71_BnzzSD1SaL8_T4lqYCa3xc2vgXQoJZF1KIx2muZOtdCYKpYB5VbsZIDg'
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


if __name__ == '__main__':
    uvicorn.run(app='server:app', reload=True)
