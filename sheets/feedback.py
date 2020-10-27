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

lessons_list = ['lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5', 'lesson_6']

def get_lesson_feedback(lesson):
	spreadsheet_id = students[0][lesson]
	# читаем шит
	spreadsheet = service.spreadsheets().get(
		spreadsheetId=spreadsheet_id,
		).execute()
	print('Get one sheet for titles')

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

	for student in students:
		spreadsheet_id = student[lesson]
		print(spreadsheet_id)
		values = service.spreadsheets().values().batchGet(
			spreadsheetId=spreadsheet_id,
			ranges=queries,
			#range=titles[1] + "!A1:YH75",
			#majorDimension='ROWS',
			).execute()
		for answer in values['valueRanges']:
			if 'values' in answer.keys():
				student_lesson = {}
				student_lesson['student_name'] = student['name']
				student_lesson['student_family'] = student['family']
				student_lesson['student_email'] = student['email']
				student_lesson['lesson'] = lesson[-1:]
				task_number = answer['range'].find('!')
				student_lesson['task'] = answer['range'][:task_number].replace("'", "")
				student_lesson['feedback'] = answer['values'][0]
				one_lesson.append(student_lesson)
		time.sleep(8)
	print('Done!')
	file_name = 'mio4_' + lesson + '.json'
	with open(file_name, 'w') as f:
		json.dump(one_lesson, f)
	return one_lesson

first_lesson = get_lesson_feedback('lesson_7')

#for one in lessons_list[:2]:
#	first_lesson = get_lesson_feedback(one)
#	file_name = 'mio4_' + one + '.json'
#	with open(file_name, 'w') as f:
#		json.dump(first_lesson, f)


