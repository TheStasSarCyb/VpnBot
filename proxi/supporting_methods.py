import os
from dotenv import load_dotenv

load_dotenv()

link = "https://px6.link/api/"+'{'+os.getenv("API_KEY_PAY")+'}/'

def ids_to_str(ids):
    str_ids = ''
    for ind in range(len(ids)-1):
        str_ids += ids[ind]+','
    str_ids += ids[-1]
    return str_ids