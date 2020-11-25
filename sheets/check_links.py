import os
import json
import time
import string
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from boto.s3.connection import S3Connection


def create_keyfile_dict():
    variables_keys = {
        "type": "service_account",
        "project_id": "sheetstest-292309",
        "private_key_id": os.environ.get('SHEETS_PRIVATE_KEY_ID'),
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDXduPfkrWiQOJV\n3A95MNpJoeMo8jmxJJEyJj6xia48J6RjZsOF0h9bmA53scBBRh2NG9t2CNqksfoj\nHOpSXgurMZDODFdB460LtZeyBfwb1q3t0rKhJZzFy5cmmJOx86MG7QbwYw28TFRa\nbwDy5yBfunfufWLgFPJsGcMiduuc6BLtM3dSTm/6zeBRwkelzWZ25/1UuCtlbg86\n2+DCVk9f5yOF3SkWf643mNJrNbGRJgQOSyMB9m3LsHGN9WnpjUXwm+zmGxNsfqfz\n4RdU2j19jm+yTJlDB0WXXtuihTgUQrMpu9FzciqiFY5Dw/dGwpoqf6GrK3Y7BWjA\nGM6BCqtLAgMBAAECggEAEHRu8KsWnf6QingU4m99rDPl0kG1cDbXs9nB3fMi0EtC\nvaiic/zZEjipmjCD+zgsl5MyDnCcqglBjh7uMj4ma/uMEIBWxZxqocNLg3f7ifC6\nNbhqle32bBChSXxLg0KVB7lgV0lpSiEWLBXgH6zRBx6JfDgtLenLnb/V7DLiyYe3\nvJIIPB9VGwjqv71+CWmfKkff89UZif+hqFDiZOcDftEX7I2HvUu7zRLw5Qt3PFj8\nP5DQmEA89YV1N6HOQHg19jn4bCEj2cInXrJvbUYeWB8tQwii5ApVPWV3DC2tj8mH\nkb8oIV/FbuwgM8+i/07WCA9uM0sirDOx77f42+RuwQKBgQD71h1gSc0mfvbMuLdS\nIECKWwOkDRg0N1IDd8wuQLwPEuVkU4U3uCPHLEgBi95yyhEzaVJHRlcpYorm/zPO\nj8LYHMXBvKMNtC/nNciKM/Kv0vWv+N5YJT3bnHKBy/wvbRN2+M/D2chAsJwTVgvZ\nHPSbD8MQNJ0rrsYvSd7KnbtgKwKBgQDbBtUxKZG+zOjwRYEf057v235YlCQQZDdg\nhK7jKOO7Uo1LT7sbAz0bH6KNqd8vPOq9fI+wJpU7N1uEQwDvX8150zntREsQQwXp\nDjR443JkEfEdUOM8Uyy7EKAdzrk6tDkJlzvaA9qQ9b4QfbYiAJZURcfBqNFmdTYP\nzjUTSmkxYQKBgQCNvItaBw9sbCbRP+EFWtuYQvNAoJIPyVbiVslW+t4dCcCLf6pJ\nmtygG58HJ8ZyCqI1skA5lzA1PZ35toZc6nJ6GW9/w4BtlQ0k7xNIHUaoiG34tXPG\nXmd7M4kK3li4BIbg/dZJX0giiIO/Kj2O24obv3pEo6gVzs8CDGxU0wODcwKBgBCY\ntfLhuX+Bu2zpd11YBcUbFrnTj+AGGAQiSbZA1PDO0pIQWpczaZ/yh7jAVH8Z2Je/\nJowsgEZabX7aLOn2knVWwh7ue9mhmoMMZoF6iqJ2kZStGmrpyovqOJfJoFOIcIH/\nibN9c0RkuqA5RmHRNZLxLq/IAQYIf6426+KoUsxBAoGBAIjUgwcyMaEUuY1rRi/W\nMHT9zHSt9FGSuhh661PFwOXZr0ay8B+4UeA4ZHqH5izzS8mVaBEOAtYBE7D/5NXG\nQ0V7S0i6FC5GOTEhSQ7G4C4aqItu/9SyIW5VY/rxDrPdlCyDlA57gk73nUBJDWpz\nT7xRNTajqJObxkbXiNXWwtPm\n-----END PRIVATE KEY-----\n",
        "client_email": "account@sheetstest-292309.iam.gserviceaccount.com",
        "client_id": os.environ.get('SHEETS_CLIENT_ID'),
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
print(credentials)

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)


#статистика текстового модуля за сентябрь
#spreadsheet_id = '1ZNFzqIpfAVdGdcp2e_e9C5NJz__-NeccbSR-Qjrr__E'

#статистика сценариев за сентябрь
spreadsheet_id = '11ErqwwqrVdJLNHKgqEuc8rsdnb3jYY1nzCnDAJb38Ug'

# читаем шит

spreadsheet = service.spreadsheets().get(
	spreadsheetId=spreadsheet_id,
).execute()

links = service.spreadsheets().values().get(
	spreadsheetId=spreadsheet_id,
	range="37!I6:I49",
	majorDimension='ROWS',
	).execute()['values']
links = [link for link in links if link]
print(links)
body = {
	'values': links,
}

new_spreadsheet_id = '15WqE31Mp8Wy2g0C5-Evklfccd2vcfra8XbDkUTDTChg'

query = service.spreadsheets().values().update(
	spreadsheetId=new_spreadsheet_id,
	valueInputOption='RAW',
	range="1!A6:A49",
	body=body,
).execute()
