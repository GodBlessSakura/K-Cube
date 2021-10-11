from config import *
import numpy as np

node = set()
link = set()
node2cate = {}
with open("../raw_data/relation.txt", 'r', encoding='utf-8') as f:
    i = 0
    for line in f.readlines():
        rela_array = line.strip("\n").split("\t")
        print(len(rela_array))
        # if len(rela_array) > 3:
        #     print("!!!!")
        i += 1
    print(i)
