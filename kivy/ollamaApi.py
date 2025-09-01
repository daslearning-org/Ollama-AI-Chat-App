import requests
import json
from kivy.clock import Clock

def get_llm_models(url):
    llm_models_url = f"{url}/api/tags"
    got_llm_models = []
    try:
        response = requests.get(llm_models_url)
        response.raise_for_status()
        models_data = response.json()
        for model in models_data.get("models", []):
            model_name = model['name']
            if model_name.find("embed") == -1: # it is not an embedding model
                got_llm_models.append(model_name)
        return got_llm_models
    except Exception as e:
        print(f"Error with Ollama: {e}")
        return got_llm_models

def chat_with_llm(url, model, messages, callback=None):
    chat_url = f"{url}/api/chat"
    msg_body = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    return_resp = {
        "role": "init",
        "content": "**Initials** in LLM response!"
    }
    try:
        response = requests.post(chat_url, json=msg_body)
        respDict = response.json()
        if "message" in respDict:
            return_resp = respDict["message"]
        else:
            return_resp = {
                "role": "error",
                "content": "**Error** in LLM response!"
            }
    except Exception as e:
        print(f"Error with Ollama: {e}")
        return_resp = {
            "role": "error",
            "content": f"**Error** with Ollama: {e}"
        }
    if callback:
        Clock.schedule_once(lambda dt: callback(return_resp))
    else:
        return return_resp

# End