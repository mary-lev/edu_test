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

#подсчет удобочитаемости
def difficulty(solutions):
	result = list()
	for all in solutions:
		if all:
			text = all[0].replace('//', ' ').replace('  ', ' ')
			print(text)
			if text:
				response = requests.post("http://api.plainrussian.ru/api/1.0/ru/measure/", data={"text":text})
				#print(response.json())
				if response.json()['indexes']['grade_SMOG'] != 'неизвестно (0)':
					result.append(response.json()['indexes']['grade_SMOG'])
			else:
				result.append("—")
	result = max(set(result), key=result.count)
	return result

def one_difficulty(text):
	response = requests.post("http://api.plainrussian.ru/api/1.0/ru/measure/", data={"text":text})
	#print(response.json())
	if response.json()['indexes']['grade_SMOG'] != 'неизвестно (0)':
		print(response.json()['indexes']['grade_SMOG'])
		return response.json()['indexes']['grade_SMOG']
	else:
		return '-'

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

for task in text_tasks:
	answers = str(task) + "!I6:I42"
	values = service.spreadsheets().values().get(
		spreadsheetId=spreadsheet_id,
		range=answers,
		majorDimension='ROWS',
		).execute()
	data[str(task)] = values
	time.sleep(2)

students_texts = dict()

with open('texts_2_indexes.json', 'r') as f:
	old_data = json.load(f)

#old_data = dict()

def get_matrix(task, student, old_data):
	all_texts = list()
	student_text = old_data[student][task]['solution'][0]
	for k, v in old_data.items():
		try:
			all_texts.append(v[task]['solution'][0])
		except:
			pass
	matrix = analyze_one(student_text, all_texts)
	print(matrix)
	return matrix


for index, student in enumerate(students):
	student_texts = list()
	all_matrix = 0
	count = 0
	df = list()
	if not student in old_data.keys():
		old_data[student] = dict()
	for task, value in data.items():
		try:
			solution = data[task]['values'][index]
			student_texts.append(solution)
			if not task in old_data[student].keys():
				old_data[student][task] = dict()
				old_data[student][task]['solution'] = solution
				if int(task) in text_tasks:
					if solution:
						df_text = one_difficulty(solution)
						old_data[student][task]['difficulty'] = df_text
			else:
				if old_data[student][task]['solution'] != solution:
					if solution:
						old_data[student][task]['solution'] = solution
					if int(task) in difficulty_tasks:
						df_text = one_difficulty(solution)
						old_data[student][task]['difficulty'] = df_text
			if int(task) in text_tasks:
				if not 'matrix' in old_data[student][task].keys() and old_data[student][task]['solution']:
					matrix = get_matrix(task, student, old_data)
					print('Matrix: ', matrix)
					all_matrix += matrix
					count += 1
					old_data[student][task]['matrix'] = matrix
				elif 'matrix' in old_data[student][task].keys():
					all_matrix += old_data[student][task]['matrix']
					count += 1
		except:
			student_texts.append([''])

		else:
			pass

	old_data[student]['tolstoy'] = count_tolstoy(student_texts)
	with open('texts_2_indexes.json', 'w') as f:
		json.dump(old_data, f)
	for k, v in old_data[student].items():
		try:
			if 'difficulty' in v.keys():
				df.append(v['difficulty'])
		except:
			pass
	result = max(set(df), key=df.count)
	if count:
		count = round(1 - all_matrix/count, 2)
	else:
		old_matrix = list()
		for k, v in old_data[student].items():
			try:
				if 'matrix' in v.keys():
					old_matrix.append(v['matrix'])
			except:
				pass
		count = round(1 - old_matrix/len(old_matrix), 2)

	students_texts[student] = [result, count_tolstoy(student_texts), count]
	print(students_texts[student])
	print(student)


title_new = 'Текстовые индексы'

#Индекс читабельности
cells = title_new + "!E6:E41"
new_values = dict()
new_values['values'] = list()

#Индекс Толстого: слова
cells_f = title_new + "!F6:F41"
values_f = dict()
values_f['values'] = list()

#ВиМ, проценты
cells_g = title_new + "!G6:G41"
values_g = dict()
values_g['values'] = list()

#матрица матриц
cells_m = title_new + "!D6:D41"
values_m = dict()
values_m['values'] = list()

for i, v in students_texts.items():
	new_values['values'].append([v[0]])
	values_f['values'].append([v[1][0]])
	values_g['values'].append([v[1][1]])
	if v[0] != '-':
		values_m['values'].append([round(v[2]*100)])
	else:
		values_m['values'].append(['-'])


query = service.spreadsheets().values().update(
		spreadsheetId=spreadsheet_id,
		valueInputOption='RAW',
		range=cells,
		body=new_values,
		).execute()

query = service.spreadsheets().values().update(
		spreadsheetId=spreadsheet_id,
		valueInputOption='RAW',
		range=cells_f,
		body=values_f,
		).execute()

query = service.spreadsheets().values().update(
		spreadsheetId=spreadsheet_id,
		valueInputOption='RAW',
		range=cells_g,
		body=values_g,
		).execute()

#matrix
query = service.spreadsheets().values().update(
		spreadsheetId=spreadsheet_id,
		valueInputOption='RAW',
		range=cells_m,
		body=values_m,
		).execute()

values = query

students = new_values
