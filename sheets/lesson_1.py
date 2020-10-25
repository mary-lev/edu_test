import json
import pandas as pd
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'sheets/creds1.json'
# ID Google Sheets документа (можно взять из его URL)
#spreadsheet_id = '1XLlJLyQP69i155tzMlMLoHZM_B83XgvTxQ6eazuFuA0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

#извлекаем данные о файлах задачника МИО 4 потока
with open('mio4.json', 'r') as f:
	students = json.load(f)

spreadsheet_id = students[0]['lesson_1']

# читаем шит
spreadsheet = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ).execute()

#извлекаем листы из шита
titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]

start_feedback = titles[0] + "!A21:E22"
help_feedback = titles[1] + "!E10:G10"
razbor = titles[1] + "!B13:B14"
#task1
task1_number = titles[2] + "!H2"
task1_text = titles[2] + "!G3:G8"
task1_image_title = titles[2] + "!B2"
task1_image = titles[2] + "!B3"
task1_answer = titles[2] + "!G10:H10"
task1_mark = titles[2] + "!K28"
task1_feedback = titles[2] + "!G31"

task2_number = titles[3] + "!H2"
task2_text = titles[3] + "!G3:G8"
task2_image = titles[3] + "!B3"
task2_answer = titles[3] + "!G10:H10"
task2_mark = titles[3] + "!K28"
task2_feedback = titles[3] + "!G31"

task3_answer = titles[4] + "!G10:G15"
task3_answer_texts = titles[4] + "!H10:H15"


#for task1_image
#values = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=task1_image, includeGridData=True).execute()
#hyperlink = values['sheets'][0]['data'][0]['rowData'][0]['values'][0]['hyperlink']

#try for task1_answer
#values = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=task1_answer, includeGridData=True).execute()

values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=task3_answer_texts,
    #range=titles[1] + "!A1:YH75",
    majorDimension='ROWS',
    ).execute()

if values['values']:
	values = values['values']

#for task1_answer
#values = values['values'][0][0]

#for task1_mark:
#values = values['values'][0][0]

#print(values)

