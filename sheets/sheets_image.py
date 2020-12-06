import json

from .drive_auth import service
from urlextract import URLExtract

# статистика по МИО-4
spreadsheet_id = '1XLlJLyQP69i155tzMlMLoHZM_B83XgvTxQ6eazuFuA0'

image_tasks = [33, 36, 40, 44, 48, 51, 61, 73, 75, 76, 94]

students = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range="0!C6:C72",
    majorDimension='ROWS',
).execute()['values']

print(students)
student_rows = zip(students, range(6, 73))
print(student_rows)

students_images = dict()

for task in image_tasks:
    range = "{task}!I6:I73".format(task=str(task))
    cells = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
        majorDimension='ROWS',
    ).execute()['values']
    extractor = URLExtract()
    answers = list()
    for cell in cells:
        if cell:
            urls = extractor.find_urls(cell[0])
            if urls:
                answers.append((students[cells.index(cell)], urls,))
    students_images[task] = answers


print(students_images)
with open('images.json', 'w') as f:
    json.dump(students_images, f)
