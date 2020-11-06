import json
import time
import string
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from sheets.from_navec import analyze_one



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

difficulty_tasks = [2, 6, 8, 12, 16, 21, 25, 29, 36, 37, 38, 46, 52, 56, 57, 60, 63, 64, 66,
					67, 68, 69, 75, 79, 80, 86, 88, 89, 90, 92, 94, 95, 97, 99, 104, 105, 106, 107, 108,
					109, 110, 111, 114, 115, 125]



#emails: C6:C42
#answers: I6:I42
students = service.spreadsheets().values().get(
	spreadsheetId=spreadsheet_id,
	range="0!C6:C42",
	majorDimension='ROWS',
	).execute()['values']

students = [all[0] for all in students]

students_texts = list()

with open('texts_2_indexes.json', 'r') as f:
	old_data = json.load(f)

def get_matrix(task, student, old_data):
	all_texts = list()
	student_text = old_data[student][task]['solution'][0]
	for k, v in old_data.items():
		all_texts.append(v[task]['solution'][0])
	matrix = analyze_one(student_text, all_texts)
	print(matrix)
	return matrix


for index, student in enumerate(students):
	student_texts = list()
	all_matrix = 0
	count = 0
	df = list()
	for task, value in old_data[student].items():
		if task in text_tasks:
			matrix = get_matrix(task, student, old_data)
			print('Matrix: ', matrix)
			all_matrix += matrix
			count += 1
			old_data[student][task]['matrix'] = matrix

	with open('texts_2_indexes.json', 'w') as f:
		json.dump(old_data, f)

	if count:
		count = all_matrix/count
		students_texts.append(count)

	print(student)


title_new = 'Текстовые индексы'

cells_m = title_new + "!D6:D41"
values_m = dict()
values_m['values'] = list()

for i in students_texts:
	values_m['values'].append([i])


def main():
#matrix
	query = service.spreadsheets().values().update(
		spreadsheetId=spreadsheet_id,
		valueInputOption='RAW',
		range=cells_m,
		body=values_m,
		).execute()

values = query

students = new_values


if __name__ == '__main__':
	main()