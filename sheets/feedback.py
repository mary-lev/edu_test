import json
import time
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



def get_lesson_feedback(lesson):
	spreadsheet_id = students[0][lesson]
	# читаем шит
	spreadsheet = service.spreadsheets().get(
		spreadsheetId=spreadsheet_id,
		).execute()

	titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
	one_lesson = list()
	if lesson == 'lesson_5':
		start_feedback = titles[0] + '!E16'
	else:
		start_feedback = titles[0] + "!E21:F21" #lessons 1-4
	help_feedback = titles[1] + "!E10:E12"
	razbor = titles[1] + "!B13:B13"

	old_ranges = {'start_feedback': start_feedback, 'help_feedback': help_feedback}

	for index, title in enumerate(titles[2:]):
		task_index = str(index+1)
		task_feedback = task_index + '_feedback'
		old_ranges[task_feedback] = title + '!G31'

	queries = [value for key, value in old_ranges.items()]
	print(queries)

	for index, student in enumerate(students):
		spreadsheet_id = student[lesson]
		print(spreadsheet_id)
		values = service.spreadsheets().values().batchGet(
			spreadsheetId=spreadsheet_id,
			ranges=queries,
			#range=titles[1] + "!A1:YH75",
			#majorDimension='ROWS',
			).execute()
			#if 'values' in values['valueRanges']:
			#	feedback[key] = values['values']
			#time.sleep(2)
		values['student_name'] = student['name']
		values['student_family'] = student['family']
		values['student_email'] = student['email']
		one_lesson.append(values)
		time.sleep(10)
	result = []
	print('Done!')
	for all in one_lesson:
		for value in all['valueRanges']:
			if 'values' in value.keys():
				new = {}
				new['student_name'] = all['student_name']
				new['student_family'] = all['student_family']
				new['student_email'] = all['student_email']
				new['lesson'] = lesson[-1:]
				task_number = value['range'].find('!')
				new['task'] = value['range'][:task_number].replace("'", "")
				new['feedback'] = value['values'][0]
				result.append(new)
	return result

#first_lesson = get_lesson_feedback('lesson_7')

lessons_list = ['lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5', 'lesson_6']

for one in lessons_list:
	first_lesson = get_lesson_feedback(one)
	file_name = 'mio4_' + one + '.json'
	with open(file_name, 'w') as f:
		json.dump(first_lesson, f)


