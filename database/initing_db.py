from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

sheet_id = "1Onid0yCQYBPAxSzI9QmrwEPG1_2StA1_cdgj27HZIso"

# Путь к твоему JSON-файлу учетной записи
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 
SERVICE_ACCOUNT_FILE = 'apis2.json'  # замени на свой путь

# Аутентификация
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Инициализация сервиса
service = build('sheets', 'v4', credentials=credentials)

current_data = {}

# Выполняем append
def append_the_data(array_data: list):
    request = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range="List1",  # Можно указать точный диапазон, например: "Лист1!A:E"
        valueInputOption='USER_ENTERED',
        body={'values': [array_data]}
    ).execute()
    
    return request

def get_last_raw():
    request = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="List1!A:A").execute()
    values = request.get("values", [])
    last_raw = len(values) + 1
    return last_raw

print(get_last_raw())