import uuid
import json
from flask.sessions import SessionInterface
from flask.sessions import SessionMixin
from itsdangerous import Signer, BadSignature, want_bytes
import math
import re
def Spno2Seat(spno):
    return str(spno % 100).zfill(2)
def Spno2Cno(spno):
    GRAD=["00","SG1","SG2","SG3","SC1","SC2","SC3","0","0","0","0","0"]
    CNO=["0","A","B","C","D","E","F","G","H","I","J"]
    cidx=math.floor(spno / 100% 10)
    gidx=math.floor(spno/1000%10)
    return f"{GRAD[gidx]}{CNO[cidx]}"

class MySession(dict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        self.sid = sid
        self.initial = initial
        super(MySession, self).__init__(initial or ())

    def __setitem__(self, key, value):
        super(MySession, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(MySession, self).__getitem__(item)

    def __delitem__(self, key):
        super(MySession, self).__delitem__(key)


class MySessionInterface(SessionInterface):
    session_class = MySession
    container = {}

    def __init__(self):
        import redis
        self.redis = redis.Redis()       

    def _generate_sid(self):
        return None

    def _get_signer(self, app):
        return None
   
    def open_session(self, app, request):
        csid = request.cookies.get(app.session_cookie_name)
        if csid  is None:
            csid = self._generate_sid()
            return self.session_class(sid=csid)
        sid=csid[4:csid.find(".")]
        list = ["sess:"+sid]
        my_bytes_value = self.redis.mget(list)[0]
        if my_bytes_value is None:
            return self.session_class(sid=csid)
        my_json = my_bytes_value.decode('utf8').replace("'", '"')
        if not "passport" in my_json:
            return self.session_class(sid=sid)
        dict = json.loads(my_json)
        if dict["passport"].get("user") is None:
            return self.session_class(sid=sid)
        dict["profile"]={}

        userid=int(dict["passport"]["user"])
        redisUser=self.redis.hget("Users",dict["passport"]["user"])
        
        if redisUser is None:
            dict["profile"] ={}
            dict["profile"]["id"]=userid
            if (userid < 1000000 and userid > 99999) or (userid<1000):
                dict["profile"]["username"]="mng"  
                dict["profile"]["Role"]="1"                        
                dict["profile"]["displayName"]="mng"
                dict["profile"]["Classno"]="None"            
                dict["profile"]["Seat"]="None" 
            else:
                classno=Spno2Cno(userid)
                seat=Spno2Seat(userid)
                dict["profile"]["Role"]="8"            
                dict["profile"]["Classno"]=classno
                dict["profile"]["Seat"]=seat
                dict["profile"]["displayName"]=f"{classno}{seat}"  
                dict["profile"]["username"]=f"{classno}{seat}"  
            return self.session_class(dict, sid=sid)

        else:
            dict["profile"] =json.loads(redisUser)
            dict["profile"] =json.loads(self.redis.hget("Users",dict["passport"]["user"]))
            result = re.search(r"S[CG][1-6][A-E]",dict["profile"]["displayName"])
            Classno="None"
            if result : Classno=result.group(0)            
            dict["profile"]["Classno"]=Classno
            dict["profile"]["Seat"]=dict["profile"]["displayName"][-2:]            
            Role="8"
            if ("SC" in Classno) or ("SG" in Classno) or ("P" in  Classno)  :
                 Role="8"            
            else:
                 Role="1"                
            dict["profile"]["Role"]=Role
            return self.session_class(dict, sid=sid)
        return self.session_class(dict, sid=sid)

    def save_session(self, app, session, response):
        pass
        #
        #val = json.dumps(dict(session))
        #keydict = {}
        #keydict['sess:'+session.sid] = val
        #self.redis.mset(keydict)
