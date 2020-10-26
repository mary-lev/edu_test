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

spreadsheet_id = students[0]['lesson_1']

# читаем шит
spreadsheet = service.spreadsheets().get(
    spreadsheetId=spreadsheet_id,
    ).execute()

#извлекаем листы из шита
titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]

first_lesson = list()
start_feedback = titles[0] + "!E21:F21"
help_feedback = titles[1] + "!E10:E11"
razbor = titles[1] + "!B13:B13"

old_ranges = {'start_feedback': start_feedback, 'help_feedback': help_feedback, 'razbor': razbor}
tasks = []
for index, title in enumerate(titles[2:]):
	task_index = str(index+1)
	task = dict()
	task_number= task_index + '_number'
	task_text = task_index + '_text'
	task_alt_text = task_index + '_2text'
	task_image_title = task_index + '_image_title'
	task_image = task_index + '_image' #!
	task_feedback = task_index + '_feedback'
	task_mark = task_index + '_mark'
	task_alt_mark = task_index + '_alt_mark'
	task_answer = task_index + '_answer'
	task_alt_answer = task_index + '_alt_answer'
	task_podskazka = task_index + '_podskazka'
	task_alt_podskazka = task_index + '_alt_podskazka'
	task_answer_labels = task_index + '_answer_labels'
	task_hyperlink = task_index + '_hyperlink'

	task[task_number] = title + '!H2'
	task[task_text] = title + '!G3:G8'
	task[task_alt_text] = title + '!H3:H8'
	task[task_image_title] = title + '!B2'
	task[task_image] = title + '!B3'
	task[task_mark] = title + '!K28'
	task[task_alt_mark] = title + '!J28'
	task[task_feedback] = title + '!G31'
	task[task_answer] = title + '!G10:H17'
	task[task_alt_answer] = title + '!J10:K17'
	task[task_podskazka] = title + '!J8:J14'
	#task[task_podskazka] = title + '!Q10:Q17'
	#task[task_alt_podskazka] = title + '!P10:P17'
	task[task_answer_labels] = title + '!J7:K7'
	task[task_hyperlink] = title + '!B3'
	tasks.append(task)


for task in tasks:
	print(task)
	new_task = dict()
	for index, name in task.items():
		if 'hyperlink' in index:
			values = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=name, includeGridData=True).execute()
			new_task[index] = values['sheets'][0]['data'][0]['rowData'][0]['values'][0]['hyperlink']
		else:
			values = service.spreadsheets().values().get(
				spreadsheetId=spreadsheet_id,
				range=name,
				#range=titles[1] + "!A1:YH75",
				majorDimension='ROWS',
				).execute()
			if 'values' in values.keys():
				new_task[index] = values['values']
	first_lesson.append(new_task)
	time.sleep(3)


task11_answer_texts = titles[10] + "!H10:H17"


#for task1_answer
#values = values['values'][0][0]

#for task1_mark:
#values = values['values'][0][0]

values = first_lesson

