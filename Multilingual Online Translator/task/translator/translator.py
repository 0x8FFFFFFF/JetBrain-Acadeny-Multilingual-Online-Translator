import sys

import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.__languages = {0: 'All', 1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew',
                            7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese',
                            11: 'Romanian', 12: 'Russian', 13: 'Turkish'}
        self.direction_from, self.direction_to, self.direction = '', '', ''
        self.translations, self.examples = [], []
        self.__run()

    def __input(self):
        if len(sys.argv) > 1:
            if len(sys.argv) != 4:
                print(f'Sorry, incorrect input of command line parameters')
                return False
            self.direction_from = sys.argv[1].capitalize()
            self.direction_to = sys.argv[2].capitalize()
            self.direction = sys.argv[1] + '-' + sys.argv[2]
            self.text = sys.argv[3]
            if self.direction_from not in self.__languages.values():
                print(f'Sorry, the program doesn\'t support {self.direction_from}')
                return False
            if self.direction_to not in self.__languages.values():
                print(f'Sorry, the program doesn\'t support {self.direction_to}')
                return False
            return True
        else:
            print("Hello, you're welcome to the translator. Translator supports:")
            for num, lang in self.__languages.items():
                print(num, lang)
            print('Type the number of your language:')
            num_lang = int(input())
            if num_lang not in range(1, 13):
                print('Sorry, incorrect translation selection')
                return False
            self.direction_from = self.__languages[num_lang]
            print('Type the number of a language you want to translate to or \'0\' to translate to all languages:')
            num_lang = int(input())
            if num_lang not in range(0, 13):
                print('Sorry, incorrect translation selection')
                return False
            self.direction_to = self.__languages[num_lang]
            self.direction = self.direction_from.lower() + '-' + self.direction_to.lower()
            print('Type the word you want to translate:')
            self.text = input()
            return True

    def __get_translate(self):
        r = requests.get(f'https://context.reverso.net/translation/{self.direction}/{self.text}',
                         headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                'Chrome/81.0.4044.129 Safari/537.36 OPR/68.0.3618.63'})
        self.status_code = r.status_code
        if self.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            self.translations = [item.text.strip('\n ') for item in soup.select("#translations-content > .translation")]
            self.examples = [item.text.strip('\n ') for item in soup.select("#examples-content .text")]
            return True
        elif self.status_code == 404:
            print(f'Sorry, unable to find {self.text}')
            return False
        else:
            print('Something wrong with your internet connection')
            return False

    def __translate(self):
        if self.__get_translate():
            print(self.status_code, 'OK')
            print('\nContext examples:')
            print(f'\n{self.direction_to} Translations:')
            for i in range(0, 5 if len(self.translations) >= 5 else len(self.translations)):
                print(self.translations[i])
            print(f'\n{self.direction_to} Examples:')
            for i in range(0, 10 if len(self.examples) >= 10 else len(self.examples), 2):
                print(self.examples[i] + ':')
                print(self.examples[i + 1] + '\n')

    def __translate_all(self):
        out_format_text = ''
        for n, language in self.__languages.items():
            if n == 0 or self.direction_from == language:
                continue
            self.direction = self.direction_from.lower() + '-' + language.lower()
            if self.__get_translate():
                out_format_text += f'{language.lower()} Translations:\n'
                out_format_text += self.translations[0] + '\n\n'
                out_format_text += f'{language.lower()} Examples:\n'
                out_format_text += self.examples[0] + ':\n'
                out_format_text += self.examples[1] + '\n\n\n'
                # sleep(0.1)
        with open(f'{self.text}.txt', 'w') as file:
            file.write(out_format_text)
        print(out_format_text)

    def __run(self):
        if self.__input():
            if self.direction_to == 'All':
                self.__translate_all()
            else:
                self.__translate()


if __name__ == '__main__':
    translator = Translator()
