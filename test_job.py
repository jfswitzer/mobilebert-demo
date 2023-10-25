import requests
import sys
SERVER_ENDPOINT=f"http://{sys.argv[1]}:5000"

def submit_bert_job(question,text):
    url = f"{SERVER_ENDPOINT}/jobsubmit"
    # hardcode the params for now
    params = {
        "question" : question,
        "text": text
    }
    resp = requests.post(url, json = params)
    resp_json = resp.json()
    print(resp_json)

if __name__ == "__main__":
    submit_bert_job("Who was Jim Henson?", "Jim Henson was a nice puppet")
    
