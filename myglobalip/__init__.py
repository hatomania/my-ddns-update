import requests as rq

def my_global_ip_address() -> str:
    res: rq.Response = rq.get("https://api.ipify.org?format=json")
    return res.json()['ip']
