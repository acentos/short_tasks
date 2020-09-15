#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from pyvirtualdisplay import Display
import csv

m_email = ""
m_pass = ""

llc_url = "https://lingualeo.com/ru/"
llc_url_vocabulary = "https://lingualeo.com/ru/dictionary/vocabulary/my"
start_time = time.time()

def ll_auth(driver):

    exist_accaunt_button = driver.find_elements_by_xpath(
        '//div[contains(text(), "У МЕНЯ УЖЕ ЕСТЬ АККАУНТ")]')

    if exist_accaunt_button:
        print(f"Auth: {exist_accaunt_button}")
        exist_accaunt_button[0].click()

    email_input = driver.find_element_by_name('email')
    password_input = driver.find_element_by_name('password')
    enter_button = driver.find_elements_by_class_name('ll-button__content')

    if ((email_input) and (password_input)):
        email_input.send_keys(m_email)
        password_input.send_keys(m_pass)
        print(f"Auth: {enter_button}")
        enter_button[0].click()
        time.sleep(4)

    if driver.current_url != llc_url_vocabulary:
        driver.get(llc_url_vocabulary)
        time.sleep(4)

def leaf_over_world(driver):

    find_first_word = driver.find_elements_by_css_selector("div.sets-words__col.sets-words__col_word")
    print(f"Leaf over: {find_first_word[0]}")
    find_first_word[0].click()
    time.sleep(4)

    word_count = 0

    while True:

        try:
            current_word = driver.find_elements_by_css_selector("div.ll-leokit__word-card__title")
            click_next_word = driver.find_elements_by_css_selector("div.ll-page-vocabulary__change-word-btn.ll-page-vocabulary__change-word-btn__m-next.ll-page-vocabulary__change-word-btn__m-active")
            print(f"Leaf over: {click_next_word[0]}")
            click_next_word[0].click()
            time.sleep(2)
            next_word = driver.find_elements_by_css_selector(
                "div.ll-leokit__word-card__title")[0].text
            next_word_transcription = driver.find_elements_by_css_selector(
                "div.ll-leokit__word-card__transcription")[0].text
            next_word_translation = driver.find_elements_by_css_selector(
                "div.ll-leokit__word-card__content")[0].text

            try:
                next_word_example = driver.find_elements_by_css_selector(
                    "div.ll-leokit__word-card__context")[0].text
            except Exception:
                next_word_example = None

            word_count +=1

            llc_list_line = [
                word_count,
                next_word,
                next_word_transcription.split(' ')[-1].replace('"', ''),
                next_word_translation.split('\n')[-1].replace('"', ''),
                next_word_example,
                next_word_image]

            print(llc_list_line)

            with open('lingualeo_vocabulary.csv', 'a') as f_obj:
                llc_writer = csv.writer(
                    f_obj, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                llc_writer.writerow(llc_list_line)

        except Exception as err:
            print(f"Leaf over error: {err}")
            continue

        if current_word == next_word:
            print(f"Leaf over: {current_word} == {next_word}")
            break

def main():

    display = Display(visible=0, size=(800, 600))
    display.start()
    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'drivers', 'chromedriver'))
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 600)
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(llc_url)
    ll_auth(driver)
    time.sleep(2)
    leaf_over_world(driver)
    driver.close()
    display.stop()

if __name__ == '__main__':
    main()
