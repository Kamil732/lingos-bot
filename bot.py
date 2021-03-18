"""
The whole code was written by Kamil Głuchowski, because
the lingos is very annoying app, so i decided to make a bot
to make the learning easier.

If you have any quiestions about this project hit me up either on messanger or github
"""

import chromedriver_autoinstaller
import codecs
import os

from random import uniform
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep

BASE_DIR = os.path.dirname('C:/')


class LingosBot:
    LOGIN_URL = 'https://lingos.pl/home/login'
    NOT_VALID_LOGIN_URL = 'https://lingos.pl/home/auth'
    # The main page where you can start lesson
    LEARNING_URL = 'https://lingos.pl/students/learning'
    CHECK_WORD_URL = 'https://lingos.pl/students/checkAnswer/0'

    def __init__(self, email, password):
        self.email = email
        self.password = password

        # Get the chromdriver for your browser
        chromedriver_autoinstaller.install()
        self.browser = webdriver.Chrome()
        self.browser.get(self.LOGIN_URL)

    def login(self):
        # Enter email
        email_input = self.browser.find_element_by_name('login')
        email_input.send_keys(self.email)

        # Enter password
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)

        if self.browser.current_url == self.NOT_VALID_LOGIN_URL:
            return False
        return True

    def edit_line(self, file, line_num, text):
        file.seek(0)  # Go to the begining of the file
        file_text = file.readlines()  # Get all lines of the file in a list
        file_text[line_num-1] = text  # Replace the line with the translation

        file.truncate(0)  # Ersing all the date in the file
        # Write the whole file with the correct translation
        file.writelines(file_text)

    def start_lesson(self, lessons=1):
        # Do from 1 to 5 lessons at once
        if lessons >= 1 and lessons <= 5:
            for _ in range(lessons):
                # Start lesson
                try:
                    start_btn = self.browser.find_element_by_xpath(
                        '//a[@href="//lingos.pl/students/learning"]')
                    start_btn.click()
                except ElementClickInterceptedException:
                    print('Już zrobiłes wszystkie lecje na dzis!')
                    break

                # Do lesson until the url change to FINISH ED_LESSON_URL
                while self.LEARNING_URL in self.browser.current_url or self.CHECK_WORD_URL in self.browser.current_url:
                    # Get word to translate
                    try:
                        learning_container = self.browser.find_element_by_xpath(
                            '//div[@id="learning-container"]')
                        word = learning_container.find_element_by_tag_name(
                            'h5').get_attribute('innerText').strip()
                    except:
                        continue

                    try:
                        with codecs.open(BASE_DIR + 'Lingos bot/words.txt', 'r+', 'utf-8') as file:
                            translated_word = ''
                            # Try to find the translated_word
                            try:
                                translated_word = learning_container.find_element_by_xpath(
                                    "//p[2]").get_attribute('innerText')

                                # Save the word with the translation if its not saved
                                is_saved = False
                                for line_num, line in enumerate(file, 1):
                                    if word == line.split('=')[0]:
                                        is_saved = True

                                if not(is_saved):
                                    file.write(f'{translated_word}={word}\n')

                                # Enter the translated word into the input
                                translated_word_input = self.browser.find_element_by_name(
                                    'answer')
                                translated_word_input.send_keys(word)

                                next_word_btn = self.browser.find_element_by_class_name(
                                    'new-btn-green')
                                sleep(3)
                                next_word_btn.click()
                                print(
                                    f'\nNowe słowo "{word} = {translated_word}" zostało zapisane\n')
                            except:
                                is_saved = False
                                for line_num, line in enumerate(file, 1):
                                    if not(is_saved) and word == line.split('=')[0]:
                                        is_saved = True
                                        guess_time = uniform(2, 5)

                                        # Try to get translated word
                                        translated_word = line.split('=')[1]
                                        learning_container = self.browser.find_element_by_xpath(
                                            '//div[@id="learning-container"]')
                                        try:
                                            help_text = learning_container.find_element_by_tag_name(
                                                'p').get_attribute("innerText").strip()
                                        except:
                                            help_text = ''

                                        if word == 'atrakcyjny' and 'Justin Bieber' in help_text:
                                            translated_word = 'good-looking'

                                        # Check if the word is translated in the words.txt
                                        if translated_word.strip() == '':
                                            is_saved = False
                                            print(
                                                '\n=========================================================')
                                            print(
                                                'BLAD: Tlumaczenie slowa nie jest zapisane \a')
                                            while translated_word.strip() == '':
                                                translated_word = str(
                                                    input(f'Podaj polskie tlmaczenie slowa "{word}": '))

                                            agree = None
                                            while not(agree == 't' or agree == 'tak'):
                                                agree = str(input(
                                                    f'Jesteś pewny, że poslkie tłumaczenie słowa "{word}" to "{translated_word}" ?\nWpisz tak[t] lub nie[n]: '))
                                                if agree == 't' or agree == 'tak':
                                                    self.edit_line(
                                                        file, line_num, f'{word}={translated_word}\n')
                                                    print(
                                                        '----- słowo zostało zapisane -----')
                                                elif not(agree == 'n' or agree == 'nie'):
                                                    # If agree is nither "no" nor "yes" then ask again if the user is sure
                                                    continue
                                                # If yes or no
                                                break

                                            if agree == 'n' or agree == 'nie':
                                                # If not then ask again about translation
                                                continue
                                            print(
                                                '\n=========================================================')

                                        # Enter the translated word into the input
                                        sleep(guess_time)
                                        translated_word_input = self.browser.find_element_by_name(
                                            'answer')
                                        translated_word_input.send_keys(
                                            translated_word)

                                        try:
                                            next_word_btn = self.browser.find_element_by_class_name(
                                                'new-btn-green')
                                        except:
                                            print(
                                                f'Tlumaczenie slowa "{word}" jest niepoprawne!')
                                            translated_word = self.browser.find_element_by_xpath(
                                                '//div[@class="main-container"]/h5[4]/span/strong').get_attribute('innerText')
                                            print(word + ' = ' + translated_word)
                                            self.edit_line(
                                                file, line_num, f'{word}={translated_word}\n')

                                            next_word_btn = self.browser.find_element_by_class_name(
                                                'new-btn-danger')

                                        sleep(2)
                                        next_word_btn.click()

                            if translated_word.strip() == '':
                                # Ask user to enter the translation of the word
                                print(
                                    '\n=========================================================')
                                print('BLAD: Slowo nie jest zapisane \a')
                                sleep(1)
                                while not(translated_word) or translated_word.strip() == '':
                                    translated_word = str(
                                        input(f'Podaj polskie tlmaczenie slowa "{word}": '))
                                print(
                                    '\n=========================================================')

                                # Check if the user agree that the translation of the word is correct
                                agree = None
                                while not(agree == 't' or agree == 'tak'):
                                    agree = str(input(
                                        f'Jesteś pewny, że poslkie tłumaczenie słowa "{word}" to "{translated_word}" ?\nWpisz tak[t] lub nie[n]: '))
                                    if agree == 't' or agree == 'tak':
                                        # If yes then write the translation into the words.txt
                                        file.write(
                                            f'{word}={translated_word}\n')
                                        print(
                                            '----- słowo zostało zapisane -----')
                                    elif not(agree == 'n' or agree == 'nie'):
                                        # If agree is nither "no" nor "yes" then ask again if the user is sure
                                        continue
                                    # If yes or no
                                    break

                                if agree == 'n' or agree == 'nie':
                                    # If not then ask again about translation
                                    continue

                    except:
                        # If user does not have the words.txt file
                        if not(os.path.exists(BASE_DIR + 'Lingos bot/words.txt')):
                            with codecs.open(BASE_DIR + 'Lingos bot/words.txt', 'w', 'utf-8') as file:
                                file.write(
                                    "To jest plik ze wszystkimi zapisanymi slówkami z ligosa :D\n\n")
                            continue

                # Close the pop up
                sleep(1)
                self.browser.find_element_by_xpath(
                    '//button[contains(text(), "ZAMKNIJ")]').click()
        else:
            print('BLAD: Nie poprawnie wprowadzona liczba lekcji')


if __name__ == '__main__':
    # limit_time = '01/03/2021'
    # past = datetime.strptime(limit_time, "%d/%m/%Y")
    # present = datetime.now()

    # if past.date() < present.date():
    #     print('\n\n\nLIMIT TWOJEGO KORZYSTANIA Z BOTa MINAŁ :) \n\nJezli chcesz korzystac z BOTa na zawsze zakup go u Kamila :D\n\n\n')
    #     input('')
    #     exit()

    # Create folder if doesn't exist yet
    if not(os.path.exists(BASE_DIR + '/Lingos bot')):
        os.makedirs(BASE_DIR + '/Lingos bot')

    # Get email and passowrd to the lingos from login.txt
    while True:
        try:
            with codecs.open(BASE_DIR + 'Lingos bot/login.txt', 'r', 'utf-8') as f:
                file = f.readline().split(',')
                EMAIL = file[0]
                PASSWORD = file[1]
        except:
            # Create a login.txt if doesn't exist
            with codecs.open(BASE_DIR + 'Lingos bot/login.txt', 'w', 'utf-8') as f:
                while True:
                    EMAIL = str(input('Podaj email do lingosa: '))
                    correct_email = str(input('Potwierdz email: '))

                    if not(EMAIL == correct_email):
                        print('\a\nEmaile nie sa takie same\n')
                        continue
                    break  # if emails are correct then pass
                print('\n')

                while True:
                    PASSWORD = str(input('Podaj haslo do lingosa: '))
                    correct_password = str(input('Potwierdz haslo: '))

                    if not(PASSWORD == correct_password):
                        print('\a\nHasla nie sa takie same\n')
                        continue
                    break  # If passwords are correct then pass

                f.write(f'{EMAIL},{PASSWORD}')  # Save login
                continue

        print('Witaj! Wlasnie wlaczyles BOTa do Lingosa\n')
        print('Slowa sa wprowadzane w przeciagu od 2 do 5 sekund, by nie bylo to podejrzane ;)')
        lessons = int(input('Podaj liczbe lekcji do wykonania od 1 do 5: '))

        # Create a Lingos Bot
        bot = LingosBot(EMAIL, PASSWORD)
        is_login_valid = bot.login()

        # Check if the login is valid
        if not(is_login_valid):
            print('Podane email lub hasło sa niepoprawne!')
            os.remove(BASE_DIR + 'Lingos bot/login.txt')
            # Remove login.txt and ask about email and password again
            continue

        try:
            bot.start_lesson(lessons)
        except:
            print('\nBLAD: Sprobuj wylaczyc i wlaczyc program\nJesli to nie zadziala to skontaktuj sie z autorem\n')
        break
