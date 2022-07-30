from project import app
from flask import request
from project.config.Database import *
from dataclasses import dataclass
from datetime import datetime

from functools import wraps

def write_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'x-auth-key' in request.headers:
            user = UserModel.query.filter_by(write_key=request.headers['x-auth-key']).first()
            if user:
                return f(user, *args, **kwargs)
            return {"status" : 403}, 403
        else:
            return {"status" : 403}, 403

    return wrap

def read_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'x-auth-key' in request.headers:
            user = UserModel.query.filter_by(read_key=request.headers['x-auth-key']).first()
            if user:
                return f(*args, **kwargs)
            return {"status" : 403}, 403
        else:
            return {"status" : 403}, 403

    return wrap

@dataclass
class NewsResponse:
    def __init__(self, model):
        self.model = model
    
    def json(self):
        return {
            "id" : self.model.id,
            "title" : self.model.title,
            "content" : self.model.content,
            "datetime" : self.model.datetime,
            "flag" : self.model.flag,
            "created_by" : self.model.created_by,
            "updated_by" : self.model.updated_by
        }


@app.route('/api/v2/news', methods = ['GET'])
@read_required
def api_index() -> dict:
    news = NewsModel.query.all()
    return {"status" : 200, "data" : [ NewsResponse(x).json() for x in news ]}

@app.route('/api/v2/news/<id>', methods = ['GET'])
@read_required
def api_news_by_id(id) -> dict:
    cekNews = NewsModel.query.filter_by(id=id).first()
    if not cekNews:
        return {"status" : 404, "msg" : "News not found"}
        
    news = NewsModel.query.filter_by(id=id).first()
    return {"status" : 200, "data" : NewsResponse(news).json() }

@app.route('/api/v2/news', methods = ['POST'])
@write_required
def api_create_news(user) -> dict:
    title = request.form['title']
    content = request.form['content']
    flag = request.form['flag']

    if flag not in ['0','1','2']:
        flag = 0

    news = NewsModel(title=title, content=content, datetime=datetime.now(), flag=flag, created_by=user.id)
    db.session.add(news)
    db.session.commit()

    return {"status" : 200, "msg" : "Success Add News"}

@app.route('/api/v2/news/<id>', methods=['PUT'])
@write_required
def api_edit_news(user, id) -> dict:
    cekNews = NewsModel.query.filter_by(id=id).first()
    if not cekNews:
        return {"status" : 404, "msg" : "News not found"}

    title = request.form['title']
    content = request.form['content']
    flag = request.form['flag']

    if flag not in ['0','1','2']:
        flag = 0

    cekNews.title = title
    cekNews.content = content
    cekNews.flag = flag
    cekNews.updated_by = user.id

    db.session.commit()
    return {"status" : 200, "msg" : "Success Edit News"}

@app.route('/api/v2/news/<id>', methods=['PATCH'])
@write_required
def api_change_flag_news(user, id):
    cekNews = NewsModel.query.filter_by(id=id).first()
    if not cekNews:
        return {"status" : 404, "msg" : "News not found"}

    flag = request.form['flag']
    if flag not in ['0','1','2']:
        flag = 0

    cekNews.flag = flag

    db.session.commit()
    return {"status" : 200, "msg" : "Success Edit Flag News"}

@app.route('/api/v2/news/<id>', methods=['DELETE'])
@write_required
def api_delete_news(user, id):
    cekNews = NewsModel.query.filter_by(id=id)
    news = cekNews.first()
    if not news:
        return {"status" : 404, "msg" : "News not found"}

    cekNews.delete()
    db.session.commit()
    return {"status" : 200, "msg" : "Success Delete News"}
