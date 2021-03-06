# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy,event


builtin_list = list


db = SQLAlchemy()



def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    displayName = db.Column(db.String(255))
    Classno = db.Column(db.String(255))
    Seat = db.Column(db.String(255))
    Role = db.Column(db.String(255))
    def __init__(self, user=None, Pass=None,Name=None,Role=None,Classno=None,Seat=None):
        self.username = user
        self.password = Pass
        self.displayName = Name
        self.Role=Role
        self.Classno=Classno
        self.Seat=Seat

    def __repr__(self):
        return "<User(User='%s', Role=%s)" % (self.user, self.Role)

def readUser(UserName):
    result = User.query.filter_by(user=UserName).first()
    #get(UserName)
    if not result:
        return None
    return from_sql(result)

#insert into user (user,Pass,Name,Role) values('admin','123','admin',1);
##
class NTEXPR(db.Model):
    __tablename__ = 'NTEXPR'
    id = db.Column(db.String(255), primary_key=True)
    nte = db.Column(db.LargeBinary)
    def __init__(self, id=None, nte=None):
        self.id= id
        self.nte =nte
    def __repr__(self):
        return "<NTEXPR(KEY='%s')" % (self.id)

def NTEList(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (NTEXPR.query
             .filter_by(Open=1)
             .order_by(NTEXPR.id)
             .limit(limit)
             .offset(cursor))
    ntexpr = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(ntexpr) == limit else None
    return (ntexpr, next_page)

def NTERead(id):
    result = NTEXPR.query.get(id)
    if not result:
        return None
    return from_sql(result)

def NTECreate(data):
    ntexpr = NTEXPR(**data)
    db.session.add(ntexpr)
    db.session.commit()
    return from_sql(ntexpr)

def NTEUpdate(data, id):
    ntexpr = NTEXPR.query.get(id)
    for k, v in data.items():
        setattr(ntexpr, k, v)
    db.session.commit()
    return from_sql(ntexpr)

def NTEDelete(id):
    NTEXPR.query.filter_by(id=id).delete()
    db.session.commit()

##
class Lesson(db.Model):
    __tablename__ = 'Lesson'
    id = db.Column(db.Integer, primary_key=True)
    Lesson = db.Column(db.String(255), unique=True)
    Title = db.Column(db.String(255))
    Path = db.Column(db.String(255), unique=True)
    Descr = db.Column(db.Text)
    logDate = db.Column(db.String(255))
    Classno = db.Column(db.String(255))
    Open = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255))
    createdById = db.Column(db.String(255))
    def __init__(self, Lesson=None, Title=None,Path=None,Classno=None,Open=None,createdById=None,Descr=None,logDate=None,imageUrl=None):
        self.Lesson= Lesson
        self.Title =Title 
        self.Path = Path 
        self.Descr =Descr 
        self.logDate=logDate
        self.Classno=Classno
        self.Open = Open 
        self.imageUrl=imageUrl
        self.createdById=createdById
    def __repr__(self):
        return "<Lesson(Lesson='%s', Title=%s)" % (self.Lesson, self.Title)


def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Lesson.query
             .filter_by(Open=1)
             .order_by(Lesson.id)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)


# [START list_by_user]
def list_by_user(user_id, limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Lesson.query
             .filter_by(createdById=user_id)
             .order_by(Lesson.Title)
             .limit(limit)
             .offset(cursor))
    lessons = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(lessons) == limit else None
    return (lessons, next_page)
# [END list_by_user]

def read(id):
    result = Lesson.query.get(id)
    if not result:
        return None
    return from_sql(result)


def create(data):
    lesson = Lesson(**data)
    db.session.add(lesson)
    db.session.commit()
    return from_sql(lesson)


def update(data, id):
    lesson = Lesson.query.get(id)
    for k, v in data.items():
        setattr(lesson, k, v)
    db.session.commit()
    return from_sql(lesson)


def delete(id):
    Lesson.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User("admin","123","admin","1")
        studa = User("stu","123","stu","8","SC1A","01")
        studb = User("sta","123","stu","8","SC2A","01")
        db.session.add(admin)
        db.session.add(studa)
        db.session.add(studb)
        db.session.commit()

    print("All tables created")
    


if __name__ == '__main__':
    _create_database()
