import base64
import requests

class Objects:
    def __init__(self):

        self.api_key = "sk-proj-3oPvOJ3IzhTGx4lMPDHLT3BlbkFJwflQxC7jarIEfphCN76R"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }


    def scan(self, image, prompt: str = "Create a list in python format of all of the objects described in one word along with their rgb value.") -> str:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=self.headers, json=self.generate_payload(prompt, image))

        return response.json()['choices'][0]['message']['content']

    def generate_payload(self, image, prompt: str) -> dict:
        return {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{self.encode_image(image)}" # Put Image Here
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }


    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def make_list(dict: dict):
        list = []
        for item, value in dict.items():
            list.append({'Desc': item, 'Color': value})
        return list

    def get_objects(self, image_path: str):
        results = eval(self.scan(prompt="You must make a list of all of the objects on the image you will receive. FORMAT LIST LIKE PYTHON DICTIONARY. Assign rgb value to each object. DON'T WRITE ANY OTHER WORDS IN YOUR RESPONSE! DO NOT ADD BACKGROUND TO LIST"), image=image_path)
        return self.make_list(results)