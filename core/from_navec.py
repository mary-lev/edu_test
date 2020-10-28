import requests
import string
import pymorphy2
from navec import Navec


path = 'data/navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)
navec = navec.as_gensim


def spellcheck(sentences):
	result = list()
	for sentence in sentences:
		old = sentence
		text = sentence.replace(' ', '+')
		url = 'https://speller.yandex.net/services/spellservice.json/checkTexts?text={0}'.format(text)
		r = requests.get(url)
		for resp in r.json()[0]:
			old_word = resp['word']
			new_word = resp['s'][0]
			old = old.replace(old_word, new_word)
		result.append(old)
	return result


def clean_all(sentences):
	clean_sentences = [all.text.replace('\n', ' ').replace('  ', ' ').replace('//', ' ').strip() for all in sentences]
	checked_sentences = spellcheck(clean_sentences)
	just_words = [all.translate(str.maketrans('', '', string.punctuation)) for all in checked_sentences]
	return just_words


def morphologize(sentences):
	list_of_sentences = [all.split(' ') for all in sentences]
	list_of_words = [[a.lower() for a in all] for all in list_of_sentences]
	morph = pymorphy2.MorphAnalyzer()
	unified_words = [[morph.parse(a)[0].normal_form for a in all] for all in list_of_words]
	return unified_words

def delete_words(sentences):
	clean_sentences = list()
	for sent in sentences:
		new = list()
		for all in sent:
			try:
				navec.word_vec(all)
				new.append(all)
			except:
				pass
		clean_sentences.append(new)
	return clean_sentences


def analyze(sentences):
	analyzed = morphologize(clean_all(sentences))
	clean_sentences = delete_words(analyzed)
	#vector_sentences = [[navec.word_vec(all) for all in sent] for sent in clean_sentences]
	matrix = []
	for sentence in clean_sentences:
		similarity = list()
		for all in clean_sentences:
			if all != sentence:
				try:
					c = navec.n_similarity(sentence, all)
					similarity.append(c)
				except:
					pass
		if len(similarity):
			matrix.append(sum(similarity)/len(similarity))
		else:
			matrix.append("А нету ничего.")
	return matrix




