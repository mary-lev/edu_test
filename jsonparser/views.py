import json
import pandas as pd

from django.shortcuts import render

from core.models import Module, Stream, Lesson, Task, Student, Solution, Feedback, Question, Variant


def index(request):
    with open('texts_2_feedback.json', 'r') as f:
        feedbacks = json.load(f)
    module = Module.objects.get(name='Тексты')
    stream = Stream.objects.get(id=3)
    for feedback in feedbacks:
        try:
            lesson_number = int(feedback['lesson'])
            lesson = Lesson.objects.get(number=int(feedback['lesson']), module=module)
        except:
            lesson = Lesson.objects.create(number=11, module=module)
        task, create = Task.objects.get_or_create(lesson=lesson, number=int(feedback['task']))
        student, create = Student.objects.get_or_create(
            email=feedback['email'],
            first_name=feedback['name'],
            last_name=feedback['family']
            )
        if stream not in student.stream.all():
            student.stream.add(stream)
        new_feedback, create = Feedback.objects.get_or_create(student=student, task=task)
        new_feedback.text = feedback['feedback']
        new_feedback.save()
    return render(request, 'index.html', {'data': feedbacks})


# parse mio lesson
def index1(request):
    with open('mio_lesson_8.json', 'r') as f:
        tasks = json.load(f)
    module = Module.objects.get(name='Информационные ожидания')
    lesson, create = Lesson.objects.get_or_create(number=7, module=module)
    for n, task in enumerate(tasks):
        task_number = n + 77
        task_image_key = str(task_number) + '_hyperlink'
        task_image_title_key = str(task_number) + '_image_title'
        task_answer_key = str(task_number) + '_answer'
        task_alt_answer_key = str(task_number) + '_alt_answer'
        task_text_key = str(task_number) + '_text'
        task_mark_key = str(task_number) + '_mark'
        task_mark_alt_key = str(task_number) + '_alt_mark'
        task_answer_label_key = str(task_number) + '_answer_labels'
        task_hint = str(task_number) + '_podskazka'
        if not task_text_key in task.keys():
            task_text_key = str(task_number) + '_2text'
        if not task_image_key in task.keys():
            task[task_image_key] = ''
        if not task_image_title_key in task.keys():
            task[task_image_title_key] = [['']]
        try:
            mark = int(task[task_mark_key][0][0])
        except:
            try:
                mark = int(task[task_mark_alt_key][0][0])
            except:
                mark = 0

        new_task, create = Task.objects.get_or_create(
            number=task_number,
            lesson=lesson)
        new_task.name=task[task_text_key][0][0]
        new_task.picture=task[task_image_key]
        new_task.picture_title=task[task_image_title_key][0][0]
        new_task.text=task[task_text_key]
        try:
            new_task.hint=task[task_hint]
        except:
            pass
        new_task.mark = mark

        if task_answer_key in task.keys():
            question, create = Question.objects.get_or_create(
                task=new_task,
                question_text=task[task_answer_key]
                )
            for var in task[task_answer_key]:
                variant, create = Variant.objects.get_or_create(
                    question=question,
                    text=var,
                    is_right=False
                    )
        elif task_alt_answer_key in task.keys():
            question, create = Question.objects.get_or_create(
                task=new_task,
                question_text=task[task_alt_answer_key],
                )
            for var in task[task_alt_answer_key]:
                variant, create = Variant.objects.get_or_create(
                    question=question,
                    text=var,
                    is_right=False
                    )
        new_task.mark = mark
        new_task.save()
    return render(request, 'index.html', {'data': tasks})


def parse4(request):
    with open('sce_solutions2.json', 'r') as f:
        solutions = json.load(f)
    for solution in solutions:
        task = Task.objects.get(number=int(solution['task']), lesson__module__name='Сценарии')
        student, create = Student.objects.get_or_create(
            first_name=solution['name'],
            last_name=solution['family'],
            email=solution['email'])
        new_solution = Solution.objects.create(task=task, student=student, text=solution['text'])
    return render(request, 'parse.html', {'data': solutions})


def parse5(request):
    with open('text_task.json', 'r') as f:
        tasks = json.load(f)
    for all in tasks:
        try:
            text_tasks = Task.objects.filter(lesson__module__name='Тексты')
            task = text_tasks.get(number=int(all['number']))
            task.name = all['title']
            task.text = all['text']
            task.save()
        except:
            print(all['number'])
    return render(request, 'parse.html', {'data': tasks})


def parse3(request):
    with open('texts2.json', 'r') as f:
        users = json.load(f)
    tasks = list()
    for all in users:
        module, create = Module.objects.get_or_create(name='Тексты')
        stream, create = Stream.objects.get_or_create(
            name='Сентябрь', module=module)
        lesson, create = Lesson.objects.get_or_create(module=module, number=int(all['lesson']))
        student, create = Student.objects.get_or_create(
            email=all['email'],
            first_name=all['name'],
            last_name=all['family']
        )
        student.stream.add(stream)
        task, create = Task.objects.get_or_create(
            number=int(all['number']), lesson=lesson)
        if all['solution']:
            solution, create = Solution.objects.get_or_create(
                task=task,
                student=student,
                text=all['solution']
            )
        if all['text']:
            feedback, create = Feedback.objects.get_or_create(
                student=student,
                task=task,
                text=all['text'])
        tasks.append(task)
    return render(request, 'parse.html', {'data': tasks})


def index1(request):
    df = pd.read_json('scenario1.json')
    users = list()
    for index, row in df.iterrows():
        module, create = Module.objects.get_or_create(
            name='Сценарии', slug='scenario')
        stream, create = Stream.objects.get_or_create(
            name='Апрель', module=module)
        student, create = Student.objects.get_or_create(
            email=row['email'],
            first_name=row['name'],
            last_name=row['last_name'])
        for x in range(1, 156):
            task, create = Task.objects.get_or_create(
                number=x,
                
                )
            if row[x]:
                feedback, create = Feedback.objects.get_or_create(
                    student=student,
                    task=task,
                    text=row[x])
        users.append(row['email'])

    return render(request, 'index.html', {'data': users})
