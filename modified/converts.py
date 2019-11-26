from string import ascii_letters
import copy
import re

# KAMUS RULE
RULE_DICT = {}

def read_grammar (grammar_file):
    # Membaca grammar dari file dan mengubahnya menjadi list
    # Mengembalikan list rules
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]

def add_rule(rule):
    # Memasukkan rule baru ke dalam kamus
    global RULE_DICT

    # mengecek apakah sudah ada head rule tsb. di dalam kamus
    if rule[0] not in RULE_DICT:
        # jika belum, tambahkan
        RULE_DICT[rule[0]] = []

    # jika sudah, tambahkan body rule
    RULE_DICT[rule[0]].append(rule[1:])

# def large(rules, let, voc):
#     # rule binarization
#     new_dict = copy.deepcopy(rules)
#     for key in new_dict:

def convert_rules():
    global RULE_DICT
    unit_productions, result = [], []
    res_append = result.append
    index = 0

    for rule in grammar:
        new_rules = []
        # skip dulu unit production
        if len(rule) == 2 and rule[1][0] != "'":
            unit_productions.append(rule)
            add_rule(rule)
            continue
        elif len(rule) > 2:
            


    # memasukkan rule ke dalam list
    grammar = read_grammar('grammar.txt')

if __name__ == '__main__':
    grammar = read_grammar('grammar.txt')
    print(read_grammar('grammar.txt'))
