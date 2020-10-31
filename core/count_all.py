import requests
import string
from urlextract import URLExtract
from natasha import MorphVocab, AddrExtractor

from .from_navec import analyze


def is_link(solutions):
	test = []
	headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36' }
	for all in solutions:
		test_url = ''
		extractor = URLExtract()
		urls = extractor.find_urls(all.text)
		for url in urls:
			if url:
				if 'http' not in url:
					url = 'http://' + url
				try:
					test_url = requests.get(url, headers=headers).status_code
				except UnicodeEncodeError:
					test_url = 'Что-то не так'
		if not urls:
			urls = 'А ссылочку?'
		test.append([all.text, urls, test_url])
	return test


def compare_texts(solutions):
	test = []
	for all in solutions:
		text = all.text
		extractor = URLExtract()
		urls = extractor.find_urls(text)
		for url in urls:
			if url:
				text = text.replace(url, '')
		text = text.split('//')
		test.append(text)
	return test


def compare_time(solutions):
	test = []
	for all in solutions:
		text = all.text.split('//')[0]
		test.append([text, dates_extractor.find(text)])
	return test

def get_address(solutions):
	test = []
	morph_vocab = MorphVocab()
	addr_extractor = AddrExtractor(morph_vocab)
	for all in solutions:
		if all.text != ' //  //  // ':
			text = all.text
			test.append([all.text, addr_extractor.find(text)])
	return test


def count_words(solutions):
	sentences = [all.text for all in solutions]
	return analyze(sentences)


def analyze_student(student):
	for all in student.solutions.all():
		task = all.task
		solutions = all.task.solutions.all()
	

#индекс удобочитаемости: https://github.com/ivbeg/readability.io/wiki/API
def difficulty(solutions):
	result = list()
	old = []
	for all in solutions:
		if all.text:
			text = all.text.replace('//', ' ').replace('  ', ' ')
			if all.text:
				response = requests.post("http://api.plainrussian.ru/api/1.0/ru/measure/", data={"text":text})
				print(response.json())
				old.append(text)
				result.append(response.json())
		else:
			result.append("Нечего считать.")
	return list(zip(old, result))


def analyze_one_student(one_student_solutions):
	return difficulty(one_student_solutions)

#Индекс Толстого
TOLSTOY = 461688
def count_tolstoy(student):
	student_text = student.solutions.all().values_list('text', flat=True)
	student_words = 0
	for all in student_text:
		s = all.translate(str.maketrans('', '', string.punctuation))
		student_words += len(s.split(' '))
	one_tolstoy = round((student_words*100)/TOLSTOY, 2)
	result = [student_words, one_tolstoy]
	return result