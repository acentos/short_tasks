import random
import sqlite3
import threading
import time
import logging
import signal
import sys
import os
import requests

start_time = time.time()
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

db_name = 'allo_prompt.db'
table_name = 'allo_grab_promt'
status_file = os.path.join(os.getcwd(), "allo_grab_promt.txt")
allo_base_url = 'https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&q='
alphabet_cyr = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
user_agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

lock = threading.Lock()

def signal_handler(signal, frame):
  with open(status_file, "w+") as fw_obj:
      fw_obj.write(str(urls))
  sys.exit(0)

def database_creator(table_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS {0} (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              product_name TEXT NOT_NULL,
              product_url TEXT,
              product_price TEXT);""".format(table_name))
    conn.commit()
    conn.close()

def uniq_random_urls(letters_num):
    logging.info("Random urls generation for {0} {1}".format(
        letters_num,
        "letter" if letters_num == 1 else "letters"))
    global urls
    urls = []
    uniq_random_letters = []
    random_letters_list = []

    for i in range(1000000):
        random_letters = ''.join(random.choices(alphabet_cyr, k=letters_num))
        random_letters_list.append(random_letters)

    uniq_random_letters = set(random_letters_list)
    with open(status_file) as cf_obj:
        status_file_content = cf_obj.read()

    for xhr_url in uniq_random_letters:
        if xhr_url not in list(status_file_content):
            urls.append(allo_base_url + xhr_url)
    logging.info("Total urls: {0}".format(len(urls) - len(list(status_file_content))))
    return urls

def insert_row_to_db(allo_xhr_result):
    conn = sqlite3.connect(db_name, timeout=60)
    cur = conn.cursor()
    for tr in allo_xhr_result.get('products'):
        try:
            lock.acquire(True)
            tr_list = []
            tr_list.append(
                (str(tr.get("name")),
                 str(tr.get("url")),
                 str(tr.get("price").split('>')[2].split('<')[0])))
            cur.executemany("""INSERT INTO {0} VALUES (NULL, ?, ?, ?)""".format(table_name),
                          tr_list)
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as err:
            print("E: {0}".format(err))
        finally:
            conn.commit()
            lock.release()
    conn.close()

def response_xhr_url(url):
    try:
        response = requests.get(url, headers=user_agent_headers)
        response.raise_for_status()
        allo_xhr_result = response.json()
        if allo_xhr_result:
            insert_row_to_db(allo_xhr_result)
    except (requests.exceptions.ConnectionError) as err:
        print("E: ", err)
    finally:
        logging.info("\"{0}\" is finishing...".format(url))

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)
    database_creator(table_name)

    if not os.path.exists(status_file):
        open(status_file, 'a').close()

    for letters_num in [1, 2, 3]:
        urls = uniq_random_urls(letters_num)

        threads = [threading.Thread(target=response_xhr_url, args=(url,)) for url in urls]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("""SELECT COUNT(*) FROM {0}""".format(table_name))
    total_db_records = ''.join(str(d) for d in cur.fetchone() if str(d).isdigit())
    conn.close()

    print("Total DB records: {0}".format(total_db_records))
    print("Total time: {0}".format(time.time() - start_time))
