import requests
import uuid
import json

def gen_data(msg, last_id):
    return {"action":"next",
        "messages":[
            {"id":str(uuid.uuid1()),"role":"user",
            "content":{"content_type":"text","parts":[msg]}}],
            "parent_message_id":last_id,"model":"text-davinci-002-render"
        }

last_id = str(uuid.uuid1())

while True:
    dat = gen_data(input(">>>"), last_id)
    s = requests.Session()
    with s.post("https://freegpt.one/backend-api/conversation", json = dat, stream=True) as r:
        res = ""
        for l in r.iter_lines():
            if l == b'data: [DONE]':
                break
            if l.startswith(b'data:'):
                res = l[5:]
        res_dict = json.loads(res)
        print("ChatGPT:")
        print(res_dict['message']['content']['parts'][0])
        last_id = res_dict['message']['id']
