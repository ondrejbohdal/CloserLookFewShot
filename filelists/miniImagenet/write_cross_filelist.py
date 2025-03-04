import numpy as np
from os import listdir
from os.path import isfile, isdir, join
import os
import json
import random
import re

cwd = os.getcwd()
data_path = join(cwd, 'images')  # 'ILSVRC2015/Data/CLS-LOC/train')
savedir = './'
dataset_list = ['base', 'val', 'novel']

#if not os.path.exists(savedir):
#    os.makedirs(savedir)

cl = -1
folderlist = []

datasetmap = {'base': 'train', 'val': 'val', 'novel': 'test'}
filelists = {'base': {}, 'val': {}, 'novel': {}}
filelists_flat = {'base': [], 'val': [], 'novel': []}
labellists_flat = {'base': [], 'val': [], 'novel': []}

for dataset in dataset_list:
    with open(datasetmap[dataset] + ".csv", "r") as lines:
        for i, line in enumerate(lines):
            if i == 0:
                continue
            fid_unused, _, label = re.split(',|\.', line)
            label = label.replace('\n', '')
            if not label in filelists[dataset]:
                fid = 0
                folderlist.append(label)
                filelists[dataset][label] = []
                fnames = listdir(join(data_path, label))
                fname_number = [int(re.split('_|\.', fname)[0][1:])
                                for fname in fnames]
                sorted_fnames = list(
                    zip(*sorted(zip(fnames, fname_number), key=lambda f_tuple: f_tuple[1])))[0]

            fname = join(data_path, label, sorted_fnames[fid])
            fid += 1
            filelists[dataset][label].append(fname)

    for key, filelist in filelists[dataset].items():
        cl += 1
        random.shuffle(filelist)
        filelists_flat[dataset] += filelist
        labellists_flat[dataset] += np.repeat(cl, len(filelist)).tolist()

#cross setting use base/val/novel together
filelists_flat_all = filelists_flat['base'] + \
    filelists_flat['val'] + filelists_flat['novel']
labellists_flat_all = labellists_flat['base'] + \
    labellists_flat['val'] + labellists_flat['novel']
fo = open(savedir + "all.json", "w")
fo.write('{"label_names": [')
fo.writelines(['"%s",' % item for item in folderlist])
fo.seek(0, os.SEEK_END)
fo.seek(fo.tell()-1, os.SEEK_SET)
fo.write('],')

fo.write('"image_names": [')
fo.writelines(['"%s",' % item for item in filelists_flat_all])
fo.seek(0, os.SEEK_END)
fo.seek(fo.tell()-1, os.SEEK_SET)
fo.write('],')

fo.write('"image_labels": [')
fo.writelines(['%d,' % item for item in labellists_flat_all])
fo.seek(0, os.SEEK_END)
fo.seek(fo.tell()-1, os.SEEK_SET)
fo.write(']}')

fo.close()
print("all -OK")
