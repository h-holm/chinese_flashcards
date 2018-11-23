import os
import re


# These are the UNICODE-numbers for characters that show up as question marks.
# Since they're invalid (for some reason), we want to remove them. We do this by
# mapping all such characters to '', meaning they'll be "translated" to nothing.
START = 55204
END = 63742
DICT_OF_RANGE = dict.fromkeys(range(START, END+1), '')
TRANSLATION_TABLE = str.maketrans(DICT_OF_RANGE)

# Pleco includes the part of speech of entries.
PARTS_OF_SPEECH_LIST = ['noun', 'adjective', 'verb', 'adverb', 'idiom', 'pronoun',
'preposition', 'conjunction', 'interjection', 'abstract noun', 'measure word']

# Pleco also includes the topic/subject of words/phrases.
VOCAB_DESCRIPTIONS_LIST = ['literary', 'linguistics', 'archaic', 'zoology',
'pejorative', 'sports', 'botany', 'Chinese medicine', 'medicine', 'dialect',
'ichthyology', 'courteous', 'polite expression', 'vulgar', 'chemistry',
'electronics', 'colloquial', 'linguistics', 'dated', 'ornithology', 'textile',
'mathematics', 'astronomy', 'internet slang', 'slang', 'anatomy', 'Buddhism',
'religion', 'philosophy', 'Taoism', 'Christianity', 'physics', 'biology',
'computing', 'geology', 'electricity', 'law', 'music', 'formal', 'informal',
'abbreviation', 'history', 'economics', 'Islam', 'Catholicism',
'transliteration', 'figurative', 'metallurgy', 'mechanics', 'well\-known phrase',
'loanword', 'mythology']

# Make a bunch of regular expressions to catch parts of speech/subjects.
VOCAB_DESCRIPTIONS_STRING = '|'.join(VOCAB_DESCRIPTIONS_LIST)
REGEX_VOCAB_DESCRIPTIONS = u'(' + VOCAB_DESCRIPTIONS_STRING + ')(?=[\s])'
REGEX_PARENTHESES_NUMBER = u'^(\([' + VOCAB_DESCRIPTIONS_STRING + u']+\) )(\d )'
REGEX_NUMBER_CHINESE = u'([0-9]{2,}[\u4e00-\u9fff]+)'
REGEX_PINYIN_CHINESE = u'([a-zA-Z]{1,1}[0-9]{1,1}(?=[\u4e00-\u9fff]))'
TIP_LINK = u'(See \w+ [\u4e00-\u9fff]+((?=[\s])|\S))'

# REGEX_PARENTHESES_NUMBER = u'^\([a-zA-Z]+\) \d '
# REGEX_PARENTHESES_NUMBER = u'^(\(' + VOCAB_DESCRIPTIONS_STRING + u'\))( )(\d)( )'
# REGEX_PARENTHESES_NUMBER = u'^(\([a-zA-Z]+\) )(\d )'


# An object of the FlashCard class represents a Pleco flashcard, i.e. the
# original Chinese entry, its translation and its pinyin (romanization).
# The part of speech as well as the subject are all "hidden" in the English
# translation and thus need to be captured.
class FlashCard(object):
    def __init__(self, chinese, pinyin, english, part_of_speech='unknown'):
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
        d = 'Part of speech:\t\t{}'.format(self.part_of_speech)
        full = a + '\n' + b + '\n' + c + '\n' + d

        return full


    # 1. Look if the entry starts with a POS from the POS list. If it does, set
    # self.part_of_speech to that POS and remove it from the entry text.
    # 2. If the entry does not start with, but contains, a POS from the POS list,
    # add the found POS (or parts of speech) to self.part_of_speech.
    def find_part_of_speech(self):
        for pos in PARTS_OF_SPEECH_LIST:
            if self.english.startswith(pos):
                self.part_of_speech = pos
                self.english = self.english[(len(pos)+1):]

        matches = {pos for pos in PARTS_OF_SPEECH_LIST if pos in self.english}
        if matches:
            for match in matches:
                if not self.part_of_speech:
                    self.part_of_speech = match
                else:
                    self.part_of_speech = self.part_of_speech + ', ' + match

        # if any(pos in self.english for pos in PARTS_OF_SPEECH_LIST):
        #     print(pos)

        return


    # Use regular expressions to clean up the entries.
    def clean_up(self):
        # Map invalid question mark characters to '', in effect removing them.
        self.english = self.english.translate(TRANSLATION_TABLE)

        # Hyperlinks in Pleco show up as a range of numbers followed by
        # duplicates of Chinese characters. We remove these.
        self.english = re.sub(REGEX_NUMBER_CHINESE, '', self.english)

        # We remove unnecessary hyperlink pinyin.
        self.english = re.sub(REGEX_PINYIN_CHINESE, r'\1 ', self.english)

        # Put vocab descriptions (i.e. the subject/topic of entries) in
        # parantheses.
        self.english = re.sub(REGEX_VOCAB_DESCRIPTIONS, r'(\1)', self.english)

        # There were a couple of double spaces in the entries.
        self.english = self.english.replace('  ', ' ')

        # This is a leftover from the hyperlinks which we want to remove.
        self.english = re.sub(TIP_LINK, r'(\1)', self.english)

        # Some entries had the vocab descriptions/topics/subjects of entries
        # before the numbers (some entries have multiple translations, i.e. 1, 2
        #, 3 et cetera). This just swaps the places of the two.
        self.english = re.sub(REGEX_PARENTHESES_NUMBER, r'\2\1', self.english)

        return


    # Entries with multiple translations will be split up so that the different
    # translations show up on separate rows in the output.
    def split_up(self, input_string):
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


def main():
    input_file_path = os.getcwd() + '/input_files/'
    directory_contents = os.listdir(input_file_path)
    for file in directory_contents:
        if file.endswith('.txt'):
            input_file = input_file_path + file

    with open(input_file, 'r') as f:
        pleco_raw_input = f.read()
        pleco_input_list = pleco_raw_input.split('\n')
        pleco_input_list = pleco_input_list[0:-1]


    card_deck = []
    for entry in pleco_input_list:
        chinese, pinyin, english = entry.split('\t', 2)
        fc = FlashCard(chinese, pinyin, english)
        card_deck.append(fc)
        print(fc)
        print()


if __name__ == "__main__":
    main()
