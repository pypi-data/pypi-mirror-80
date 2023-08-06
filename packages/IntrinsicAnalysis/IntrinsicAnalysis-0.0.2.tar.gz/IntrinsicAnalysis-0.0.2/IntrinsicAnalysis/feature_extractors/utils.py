import re
import os
import stanza
import spacy_udpipe

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

EXTERNAL_DIR = ROOT_DIR+'/external_data'
STANZA_MODEL_HY = '/tmp/intrinsic_analysis/essential_models/'
UDPIPE_MODEL_HY = '/tmp/intrinsic_analysis/essential_models/armenian-armtdp-ud-2.5-191206.udpipe'

nlp_udpipe = spacy_udpipe.load_from_path(lang='hy', path=UDPIPE_MODEL_HY,
                                         meta={"description": "Custom hy model"})

nlp_stanza = stanza.Pipeline(use_gpu=False, lang='hy', dir=STANZA_MODEL_HY,
                             processors='tokenize, mwt, pos, lemma, depparse')


def lemmatizer(text: str):
    doc = nlp_stanza(text)
    return [word.lemma for sentence in doc.sentences for word in sentence.words]


def pos_tagger(text: str):
    doc = nlp_stanza(text)
    return [word.pos for sentence in doc.sentences for word in sentence.words]


def word_tokenize(text: str, remove_punctuation=False):
    text = remove_punct(text) if remove_punctuation else text
    doc = nlp_udpipe(text)
    return [word.text for word in doc]


def letter_tokenize(text: str):
    return list(re.sub(r'[^\u0561-\u0587\u0531-\u0556]', '', text))


def letters_and_numbers(text: str):
    return list(re.sub(r'[^\d\u0561-\u0587\u0531-\u0556]', '', text))


def remove_punct(text: str):
    return re.sub(r'[^\d\s\u0561-\u0587\u0531-\u0556]', ' ', text)


def remove_non_letters(text: str):
    return re.sub(r'[^\s\u0561-\u0587\u0531-\u0556]', ' ', text)

def sentence_tokenize(text: str):
    doc = nlp_udpipe(text)
    return [x.string for x in list(doc.sents)]


def syllables_counter(text: str):
    c = Counter(text)
    return c["ա"] + c["ե"] + c["է"] + c["ը"] + c["ի"] + c["ո"] + c["և"] + c["օ"]
