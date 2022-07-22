import re

# from pydantic import ValidationError

# with open("bad_words.txt") as f:
#     # ls = list
#     # for i in f:
#     #     ls.append(i)
#     # print(ls)
#     ls = list()
#     for i in f:
#         ls.append(i)
# ls2 = list()
# for i in ls:
#     idx = i.find('=')
#     # end_line = i.find('\n')
#     ls2.append(i[:idx])
# print(ls2)


# ls2 = list()
# for i in ls:
#     idx = i.find('=')
#     # end_line = i.find('\n')
#     ls2.append(i[:idx])
#     CENSORED_WORDS = f.readlines()
#     CENSORED_WORDS.find('\n')
#     print(CENSORED_WORDS)


with open("bad_words.txt") as f:
    ls = list()
    for i in f:
        ls.append(i)
ls2 = list()
for i in ls:
    idx = i.find('=')
    ls2.append(i[:idx])


def comment_filter(body: str) -> str:
    for word in ls2:
        body = body.replace(word, '*'*len(word))
    return body



# import os
# import inflection
#
#
#
#
# # with open("bad_words.txt") as f:
# #     CENSORED_WORDS = f.readlines()
# #
# # def validate_comment_text(text):
# #     words = set(re.sub("[^\w]", " ",  text).split())
# #     if any(censored_word in words for censored_word in CENSORED_WORDS):
# #         raise ValidationError(f"{censored_word} is censored!")
#
#
# class ProfanityFilter:
#     def __init__(self,**kwargs):
#         self._custom_censor_list = kwargs.get('custom_censor_list', [])
#         self._extra_censor_list = kwargs.get('extra_censor_list', [])
#         self._censor_list = []
#         self._censor_char = "*"
#         self._BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#
#         self._words_file = os.path.join(self._BASE_DIR, 'bad_words.txt')
#         self._load_words()
#
#     def _load_words(self):
#         """ Loads the list of profane words from file. """
#         with open(self._words_file, 'r') as f:
#             self._censor_list = [line.strip() for line in f.readlines()]
#
#     def define_words(self, word_list):
#         """ Define a custom list of profane words. """
#         self._custom_censor_list = word_list
#
#     def append_words(self, word_list):
#         """ Extends the profane word list with word_list """
#         self._extra_censor_list.extend(word_list)
#
#     def set_censor(self, character):
#         """ Replaces the original censor character '*' with character """
#         if isinstance(character, int):
#             character = str(character)
#         self._censor_char = character
#
#     def has_bad_word(self, text):
#         """ Returns True if text contains profanity, False otherwise """
#         return self.censor(text) != text
#
#     def get_custom_censor_list(self):
#         """ Returns the list of custom profane words """
#         return self._custom_censor_list
