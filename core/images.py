import json
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'edu_test.settings'
django.setup()

from .models import Student, Task, Image


with open('images.json', 'r') as f:
    data = json.load(f)

for task, answers in data.items():
    find_task = Task.objects.get(lesson__module__name="Информационные ожидания", number=task)
    print(find_task)
    for answer in answers:
        student, create = Student.objects.get_or_create(email=answer[0][0])
        print(student)
        for im in answer[1]:
            print(im)
            image = Image.objects.create(student=student, task=find_task, url=im)