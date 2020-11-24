import os
import json
import time
import string
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


def create_keyfile_dict():
    variables_keys = {
        "type": "service_account",
        "project_id": "sheetstest-292309",
        "private_key_id": os.environ['SHEETS_PRIVATE_KEY_ID'],
        "private_key": os.environ['SHEETS_PRIVATE_KEY'],
        "client_email": "account@sheetstest-292309.iam.gserviceaccount.com",
        "client_id": os.environ['SHEETS_CLIENT_ID'],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url":  "https://www.googleapis.com/robot/v1/metadata/x509/account%40sheetstest-292309.iam.gserviceaccount.com"
    }
    return variables_keys



scope = ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive']

try:
	credentials = ServiceAccountCredentials.from_json_keyfile_dict(
		create_keyfile_dict(),
		scope
		)
except:
	CREDENTIALS_FILE = 'sheets/sheetstest.p12'
	CREDENTIALS_EMAIL = 'account@sheetstest-292309.iam.gserviceaccount.com'
	KEY = 'notasecret'
	credentials = ServiceAccountCredentials.from_p12_keyfile(
		CREDENTIALS_EMAIL,
		CREDENTIALS_FILE,
		KEY,
		scope,
		)


httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


#статистика текстового модуля за сентябрь
#spreadsheet_id = '1ZNFzqIpfAVdGdcp2e_e9C5NJz__-NeccbSR-Qjrr__E'

#статистика сценариев за сентябрь
spreadsheet_id = '11ErqwwqrVdJLNHKgqEuc8rsdnb3jYY1nzCnDAJb38Ug'

# читаем шит
def main():
	spreadsheet = service.spreadsheets().get(
		spreadsheetId=spreadsheet_id,
		).execute()

	links = service.spreadsheets().values().get(
		spreadsheetId=spreadsheet_id,
		range="37!I6:I49",
		majorDimension='ROWS',
		).execute()['values']

	return links


if __name__ == '__main__':
	links = main()
	for link in links:
		print(link)