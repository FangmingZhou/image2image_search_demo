import os

from constant import *

def readImageSet(collection, dataset=None, rootpath=ROOT_PATH):
    if not dataset:
        dataset = collection
    imsetfile = os.path.join(rootpath, collection, 'ImageSets', '%s.txt' % dataset)
    imset = map(str.strip, open(imsetfile).readlines())
    assert(len(imset[0].split())==1), 'invalid image-id %s' % imset[0]
    return imset

def readVideoSet(collection, dataset=None, rootpath=ROOT_PATH):
    if not dataset:
        dataset = collection
    imsetfile = os.path.join(rootpath, collection, 'VideoSets', '%s.txt' % dataset)
    imset = map(str.strip, open(imsetfile).readlines())
    assert(len(imset[0].split())==1), 'invalid image-id %s' % imset[0]
    return imset
