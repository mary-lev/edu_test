import pandas as pd
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'sheets/creds1.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1XLlJLyQP69i155tzMlMLoHZM_B83XgvTxQ6eazuFuA0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# Пример чтения файла
spreadsheet = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ).execute()

titles = []

for sheet in spreadsheet['sheets']:
    titles.append(sheet['properties']['title'])

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=titles[0]+"!A1:Y75",
    majorDimension='ROWS'
    ).execute()

columns = values['values'][4] + ['proc']
df = pd.DataFrame.from_records(values['values'][5:], columns=columns)
df = df.to_html()
