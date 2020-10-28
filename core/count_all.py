from urlextract import URLExtract
import requests
from .from_navec import analyze

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)


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
			else:
				test_url = 'А ссылочку?'
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
	for all in solutions:
		if all.text != ' //  //  // ':
			text = all.text
			test.append([all.text, addr_extractor.find(text)])
	return test


def count_words(solutions):
	sentences = [all.text for all in solutions]
	return zip(sentences, analyze(solutions))

