#!/usr/bin/env python

import sys
import os

big_file = "vocabulary_all.txt"
html_file = "Словарь.html"
try:
    out_file = sys.argv[1]
    open(out_file, 'a').close()
    try:
        with open(html_file, "r") as f_obj:
            file_datas = f_obj.readlines()
    except FileNotFoundError:
        sys.exit("HTML file {} not found".format(html_file))

    vocabulary = {}
    for file_data in file_datas:
        if '<strong class="sets-words__my-word">' in file_data:
            split_line_w1 = file_data.split('<')
            split_line_w2 = split_line_w1[1]
            word = split_line_w2.split('>')[1]
            split_line_w3 = split_line_w1[5]
            transplate = split_line_w3.split('>')[1]
            vocabulary[word] = transplate

    line_num = 1
    for w_key, w_value in vocabulary.items():
        print("{0} {1} - {2}".format(line_num, w_key, w_value))
        with open(out_file, "a") as v_obj:
            v_obj.write("\n{0} {1} - {2}".format(line_num, w_key, w_value))
        line_num += 1
    if os.path.join(os.getcwd(), out_file):
        os.system("cat {0} >> {1}".format(out_file, big_file))

except IndexError:
    sys.exit("Run like it: python {0} your_filename.txt".format(sys.argv[0]))
