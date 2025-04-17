import requests
from dotenv import load_dotenv
import os, json


def load_env():
    env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        raise Exception("Файл .env не найден!")


def get_models(token: str):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get("https://api.gpt.mws.ru/v1/models", headers=headers)
    return response.json()


def print_json(json_data):
    print(json.dumps(json_data, indent=4, ensure_ascii=False))


def select_model(token: str):
    models_data = get_models(token)
    models_names = [el["id"] for el in models_data["data"]]

    print("Доступные модели:")
    for i, model in enumerate(models_names):
        print(f"[{i}] {model}")
    cur_model_id = int(input("\nВыберите модель, с которой хотите взаимодействовать: "))

    if not (0 <= cur_model_id < len(models_names)):
        raise Exception("Неправильный номер!")

    return models_names[cur_model_id]


def send_prompt(model: str, token: str, messages: list = []):
    headers = {"Authorization": f"Bearer {token}"}
    
    with open("./prompt.txt", "r", encoding="UTF-8") as p_file:
        main_prompt = p_file.read()
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": main_prompt},
            *messages,
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.gpt.mws.ru/v1/chat/completions", json=data, headers=headers)
    return response.json()
