import web
import os, sys, random
import json

from util import readImageSet

from simpleknn.simpleknn import load_model
from simpleknn.bigfile import BigFile

from images import images, bigimages, queryimages

urls = (
    '/', 'index',
    '/search', 'ImageSearch',
    '/images/(.*)', 'images',
    '/img/(.*)', 'images',
    '/images2/(.*)', 'bigimages',
    '/queryimages/(.*)', 'queryimages',
)
       
render = web.template.render('templates/')
config = json.load(open('config.json'))

max_hits = config['max_hits']
rootpath = config['rootpath']
trainCollection = config['trainCollection']
testCollection = config['testCollection']
feature = config['feature']
distance = config['distance']
rankMethod = ""


class index:
    
    def GET(self):
        input = web.input(query=None)
        resp = {'status':0, 'hits':0, 'random':[], 'tagrel': []}

        if input.query:
            resp['status'] = 1
            resp['query'] = input.query.strip()

            vec = web.test_feat_file.read_one(resp['query'])
            ranklist = web.searcher.search_knn(vec, max_hits=100)

            resp['hits'] = len(ranklist)
            content = []
            for name, score in ranklist:
                color = 'white'
                res = {'id':name, 'color':color, 'tags':''}
                content.append(res)
            resp['tagrel'] = content[:max_hits]
        else:
            selected = random.sample(web.imset, max_hits)
            resp['random'] = [{'id':x, 'color':'white'} for x in selected] 
        return render.index(resp)


class ImageSearch:
    def POST(self):
        input = web.input()
        raise web.seeother('/?query=%s' % input.query)


        
if __name__ == "__main__":
    app = web.application(urls, globals())

    test_feat_dir = os.path.join(rootpath, testCollection, 'FeatureData', feature)
    web.test_feat_file = BigFile(test_feat_dir)

    train_feat_dir = os.path.join(rootpath, trainCollection, 'FeatureData', feature)
    web.searcher = load_model(train_feat_dir)
    web.searcher.set_distance(distance)

    web.imset = readImageSet(testCollection, testCollection, rootpath)

    app.run()
