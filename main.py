import requests
import os
import json

from functions import *

load_env()
TOKEN = os.environ.get("MWS_GPT")

if __name__ == "__main__":
    cur_model = select_model(TOKEN)
    messages = []

    while True:
        prompt = input("User:\n")
        messages.append({"role": "user", "content": prompt})

        result = send_prompt(cur_model, TOKEN, messages)["choices"][0]["message"]["content"]

        messages.append({"role": "assistant", "content": result})
        
        print(f"\nAssistant: \n{result}\n")