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
	first_lesson = list()
	start_feedback = titles[0] + "!E21:F21"
	help_feedback = titles[1] + "!E10:E11"
	razbor = titles[1] + "!B13:B13"

	old_ranges = {'start_feedback': start_feedback, 'help_feedback': help_feedback}

	for index, title in enumerate(titles[2:]):
		task_index = str(index+1)
		task_feedback = task_index + '_feedback'
		old_ranges[task_feedback] = title + '!G31'

	queries = [value for key, value in old_ranges.items()]

	for index, student in enumerate(students):
		spreadsheet_id = student[lesson]
		print(spreadsheet_id)
		try:
			values = service.spreadsheets().values().batchGet(
				spreadsheetId=spreadsheet_id,
				ranges=queries,
				#range=titles[1] + "!A1:YH75",
				#majorDimension='ROWS',
				).execute()
				#if 'values' in values['valueRanges']:
				#	feedback[key] = values['values']
				#time.sleep(2)
			values['student'] = index
			first_lesson.append(values)
		except:
			pass
	result = []
	for all in first_lesson:
		for value in all['valueRanges']:
			if 'values' in value.keys():
				new = {}
				new['student'] = all['student']
				new['lesson'] = '2'
				task_number = value['range'].find('!')
				new['task'] = value['range'][:task_number].replace("'", "")
				new['feedback'] = value['values'][0]
				result.append(new)
	return result

first_lesson = get_lesson_feedback('lesson_2')

with open('mio4_lesson2.json', 'w') as f:
	json.dump(first_lesson, f)


