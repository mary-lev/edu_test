import json
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
    #range=titles[1] + "!A1:YH75",
    majorDimension='ROWS'
    ).execute()

#for summary sheet
columns = values['values'][4] + ['proc']

def extract_id(filename):
    start = len('https://docs.google.com/spreadsheets/d/')
    end = filename.find('/edit?usp=sharing')
    file_id = filename[start:end]
    return file_id

df = pd.DataFrame.from_records(values['values'][5:], columns=columns)
#df = pd.DataFrame.from_records(values['values'])
students = []
for index, row in df.iterrows():
    if row['1 урок']:
        student = {}
        student['name'] = row['Имя']
        student['family'] = row['Фамилия']
        student['email'] = row['Email']
        student['lesson_1'] = extract_id(row['1 урок'])
        student['lesson_2'] = extract_id(row['2 урок'])
        student['lesson_3'] = extract_id(row['3 урок'])
        student['lesson_4'] = extract_id(row['4 урок'])
        student['lesson_5'] = extract_id(row['5 урок'])
        student['lesson_6'] = extract_id(row['6 урок'])
        student['lesson_7'] = extract_id(row['7 урок'])
        student['lesson_8'] = extract_id(row['8 урок'])
        student['lesson_9'] = extract_id(row['9 урок'])
        student['lesson_0'] = extract_id(row['0 урок'])
        students.append(student)

with open('mio4.json', 'w') as f:
    json.dump(students, f)

df = df.to_html()
