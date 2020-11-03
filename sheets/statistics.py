import json
import time
import string
import requests
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


#статистика текстового модуля за сентябрь
spreadsheet_id = '1ZNFzqIpfAVdGdcp2e_e9C5NJz__-NeccbSR-Qjrr__E'

# читаем шит
spreadsheet = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ).execute()

#извлекаем листы из шита
titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
text_tasks = [2, 6, 8, 12, 16, 21, 24, 25, 29, 30, 31, 32, 33, 36, 37, 38, 46, 48, 50, 52, 56, 
			57, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 73, 75, 76, 79, 80, 86, 88, 89, 90, 92,
			94, 95, 97, 98, 99, 104, 105, 106, 107, 108, 109, 110, 111, 114, 115, 120, 123, 125,
			126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 144, 
			145, 146, 147, 149, 150, 151, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165]

#подсчет удобочитаемости
def difficulty(solutions):
	result = list()
	for all in solutions:
		if all:
			text = all[0].replace('//', ' ').replace('  ', ' ')
			print(text)
			if text:
				response = requests.post("http://api.plainrussian.ru/api/1.0/ru/measure/", data={"text":text})
				print(response.json())
				if response.json()['indexes']['grade_SMOG'] != 'неизвестно (0)':
					result.append(response.json()['indexes']['grade_SMOG'])
		else:
			result.append("Нечего считать.")
	result = max(set(result), key=result.count)
	return result

#Индекс Толстого
TOLSTOY = 461688
def count_tolstoy(solutions):
	student_words = 0
	for all in solutions:
		if all:
			s = all[0].translate(str.maketrans('', '', string.punctuation))
			student_words += len(s.split(' '))
	one_tolstoy = round((student_words*100)/TOLSTOY, 2)
	result = [student_words, one_tolstoy]
	return result

#emails: C6:C42
#answers: I6:I42
students = service.spreadsheets().values().get(
	spreadsheetId=spreadsheet_id,
	range="0!C6:C42",
	majorDimension='ROWS',
	).execute()['values']

students = [all[0] for all in students]
data = dict()

for task in text_tasks[:5]:
	answers = str(task) + "!I6:I42"
	values = service.spreadsheets().values().get(
		spreadsheetId=spreadsheet_id,
		range=answers,
		majorDimension='ROWS',
		).execute()
	data[str(task)] = values
	time.sleep(2)

students_texts = dict()

for index, student in enumerate(students):
	student_texts = list()
	for task, value in data.items():
		try:
			student_texts.append(data[task]['values'][index])
		except:
			student_texts.append([''])
	students_texts[student] = [difficulty(student_texts), count_tolstoy(student_texts)]


title_new = 'Текстовые индексы'
cells = title_new + "!E6:E41"
#new_values = [{'values': [[value[0]]]} for key, value in students_texts.items()]
new_values = dict()
new_values['values'] = list()

new_cells = title_new + "!D6:D41"
values_d = dict()

for i, v in students_texts.items():
	new_values['values'].append([v[0]])
	values_d['values'].append([v[1]])


query = service.spreadsheets().values().update(
	spreadsheetId=spreadsheet_id,
	valueInputOption='RAW',
	range=cells,
	body=new_values,
	).execute()

query = service.spreadsheets().values().update(
	spreadsheetId=spreadsheet_id,
	valueInputOption='RAW',
	range=new_cells,
	body=values_d,
	).execute()


values = query

students = new_values


