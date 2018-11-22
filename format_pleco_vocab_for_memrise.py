import os
import re


START = 55204
END = 63742
DICT_OF_RANGE = dict.fromkeys(range(START, END+1), '')
TRANSLATION_TABLE = str.maketrans(DICT_OF_RANGE)

REGEX_NUMBER_CHINESE = u'([0-9]{2,}[\u4e00-\u9fff]+)'
REGEX_PINYIN_CHINESE = u'([a-zA-Z]{1,1}[0-9]{1,1}(?=[\u4e00-\u9fff]))'

VOCAB_DESCRIPTIONS_LIST = ['literary', 'linguistics', 'archaic', 'zoology',
'pejorative', 'sports', 'botany', 'medicine', 'transliteration', 'dialect',
'ichthyology', 'courteous', 'polite expression', 'vulgar', 'chemistry',
'electronics', 'colloquial', 'linguistics', 'dated', 'ornithology', 'textile',
'mathematics', 'astronomy']
VOCAB_DESCRIPTIONS_STRING = '|'.join(VOCAB_DESCRIPTIONS_LIST)
REGEX_VOCAB_DESCRIPTIONS = u'(' + VOCAB_DESCRIPTIONS_STRING + ')'

TIP_LINK = u'(See \w+ [\u4e00-\u9fff]+((?=[\s])|\S))'

REGEX_PARENTHESES_NUMBER = u'^\([a-zA-Z]+\) \d '
# REGEX_PARENTHESES_NUMBER = u'^(\(' + VOCAB_DESCRIPTIONS_STRING + u'\))( )(\d)( )'
REGEX_PARENTHESES_NUMBER = u'^(\([a-zA-Z]+\) )(\d )'

class FlashCard(object):
    PART_OF_SPEECH = ('noun', 'adjective', 'verb', 'adverb', 'idiom', 'pronoun',
                      'preposition', 'conjunction', 'interjection', 'article',
                      'abstract noun', 'collective noun', 'measure word')


    def __init__(self, chinese, pinyin, english, part_of_speech=None):
        self.chinese = chinese
        self.pinyin = pinyin
        self.english = english
        self.part_of_speech = part_of_speech
        self.find_part_of_speech()
        self.clean_up()
        self.english = self.split_up(self.english)


    def __repr__(self):
        a = 'Chinese entry:\t\t{}'.format(self.chinese)
        b = 'Pinyin:\t\t\t{}'.format(self.pinyin)
        c = 'English translation:\t{}'.format(self.english)
        full = a + '\n' + b + '\n' + c
        if self.part_of_speech:
            d = 'Part of speech:\t\t{}'.format(self.part_of_speech)
            full = full + '\n' + d
        else:
            d = 'Part of speech:\t\tunknown'
            full = full + '\n' + d

        return full


    def find_part_of_speech(self):
        if self.english.startswith(self.PART_OF_SPEECH):
            if self.english.startswith('noun'):
                self.part_of_speech = 'noun'
                self.english = self.english[len('noun '):]
            if self.english.startswith('adjective'):
                self.part_of_speech = 'adjective'
                self.english = self.english[len('adjective '):]
            if self.english.startswith('verb'):
                self.part_of_speech = 'verb'
                self.english = self.english[len('verb '):]
            if self.english.startswith('adverb'):
                self.part_of_speech = 'adverb'
                self.english = self.english[len('adverb '):]
            if self.english.startswith('idiom'):
                self.part_of_speech = 'idiom'
                self.english = self.english[len('idiom '):]

        return

    def clean_up(self):
        self.english = self.english.translate(TRANSLATION_TABLE)

        # print(self.english)
        self.english = re.sub(REGEX_NUMBER_CHINESE, '', self.english)
        # print(self.english)
        self.english = re.sub(REGEX_PINYIN_CHINESE, r'\1 ', self.english)
        # print(self.english)
        self.english = re.sub(REGEX_VOCAB_DESCRIPTIONS, r'(\1)', self.english)
        # print(self.english)
        self.english = self.english.replace('  ', ' ')
        # print(self.english)
        self.english = re.sub(TIP_LINK, r'(\1)', self.english)
        # print(self.english)
        if re.search(REGEX_PARENTHESES_NUMBER, self.english):
            print('MATCH', self)

        # self.english = re.sub(r'(parenthesis)(.*)(1)', r'\3\2\1', self.english)
        self.english = re.sub(REGEX_PARENTHESES_NUMBER, r'\2\1', self.english)

        return

    def split_up(self, input_string):
        print(input_string)
        if is_int(input_string[0]) and input_string[1] == ' ':
            # look_for_string = ' ' + str(int(input_string[0])+1) + ' '
            # print(look_for_string)
            # idx = input_string.index(look_for_string)
            match = re.search(' \d ', input_string)
            if match:
                idx = match.start()
                s1 = input_string[0:idx+1]
                s2 = input_string[idx+1:]
                s2 = self.split_up(input_string[idx+1:])
                input_string = s1.strip() + ';\n\t\t\t' + s2

        return input_string


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


input_file_path = os.getcwd() + '/input_files/'


directory_contents = os.listdir(input_file_path)
# print(directory_contents)


for file in directory_contents:
    if file.endswith('.txt'):
        input_file = input_file_path + file


with open(input_file, 'r') as f:
    pleco_raw_input = f.read()
    pleco_input_list = pleco_raw_input.split('\n')
    pleco_input_list = pleco_input_list[0:-1]


# TODO: Vissa pinyin blir fel, t ex Zhou4 Xin1 och Wei4 Jin4
card_deck = []
for entry in pleco_input_list:
    chinese, pinyin, english = entry.split('\t', 2)
    # card_deck.append(FlashCard(chinese, pinyin, english))
    fc = FlashCard(chinese, pinyin, english)
    card_deck.append(fc)
    # print(entry)
    print(fc)
    print()
