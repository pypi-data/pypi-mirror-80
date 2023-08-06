from similarity import compare
import glob
import os
import json
import numpy as np
def run():
    source = 'main_image\\main.jpg'
    titles = []
    for f in glob.iglob("images\*"):
        titles.append(f)
    print(*titles)
    d = {os.path.basename(source) :
                                    { os.path.basename(img): 0  for img in titles   
            }}
    for i in titles:
        p = compare(source,i)
        d[os.path.basename(source)][os.path.basename(i)] = p


    with open("info.json", "w") as write_file:
            json.dump(d, write_file)
