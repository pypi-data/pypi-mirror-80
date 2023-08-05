import requests
from kmon_code import KmonException
import code_def
import numpy as np
import json

class Kmon:
    backend_addr = None
    token = None
    headers = None
    __is_valid_token = False

    def __init__(self,url):
        try:
            self.backend_addr = url
            if self.backend_addr[len(self.backend_addr)-1] == '/':
                self.backend_addr = self.backend_addr[:-1]
            self.__req('/api/verifyToken','POST')
        except Exception:
            raise

    def set_token(self,token):
        try:
            self.token = token
            self.headers = {'Authorization': 'Bearer ' + token}
            res = self.__req('/api/verifyToken','POST')
            if res != None and res.status_code != 200: raise KmonException(code_def.INVALID_HTTP_REQUEST)
            # data = res.json()
            # if data.code != code_def.SUCCESS: raise KmonException(res.code,res.message,res.data)
            self.__is_valid_token = True; 
            return True
        except KmonException:
            raise            
        except Exception:
            raise
    
    def job_init(self,type,params,space=''):
        try:
            if self.__is_valid_token == False: raise KmonException(code_def.NOT_SET_TOKEN)
            params = self.__np2dict(params)
            data = { "type" : type, "params" : params, "space" : space , "token" : self.token}            
            res = self.__req('/api/job/init','POST',data)
            if res != None and res.status_code != 200: raise KmonException(code_def.INVALID_HTTP_REQUEST)
            data = res.json()
            if data['code'] != code_def.SUCCESS.code: raise KmonException(data['code'],data['message'],data['data'])
            return data['data']['key']
        except KmonException:
            raise
        except Exception:
            raise

    def job_next(self,key):
        try:
            if self.__is_valid_token == False: raise KmonException(code_def.NOT_SET_TOKEN)
            data = { "key" : key}
            res = self.__req('/api/job/next','POST',data)
            if res != None and res.status_code != 200: raise KmonException(code_def.INVALID_HTTP_REQUEST)
            data = res.json()
            if data['code'] != code_def.SUCCESS.code: raise KmonException(data['code'],data['message'],data['data'])
            return self.__dict2np(data['data']['rho'])
        except KmonException :
            raise
        except Exception:
            raise

    def job_feedback(self,key,rho,obs):
        try:
            if self.__is_valid_token == False: raise KmonException(code_def.NOT_SET_TOKEN)
            rho = self.__np2dict(rho)
            obs = self.__np2dict(obs)
            data = { "key" : key, 'rho' : rho, 'obs' : obs}
            res = self.__req('/api/job/feedback','POST',data)
            if res != None and res.status_code != 200: raise KmonException(code_def.INVALID_HTTP_REQUEST)
            data = res.json()
            if data['code'] != code_def.SUCCESS.code: raise KmonException(data['code'],data['message'],data['data'])
            return data['data']['feedback']
        except KmonException:
            raise
        except Exception:
            raise
    
    def __req(self,path, method, data={}):
        url = self.backend_addr + path
            
        if method == 'GET':
            return requests.get(url, headers=self.headers)
        else:
            return requests.post(url, headers=self.headers, json=data)

    def __np2dict(self,obj):
        if isinstance(obj, np.ndarray): return obj.tolist()
        elif isinstance(obj, dict): 
            for key, val in obj.items():
                try: json.dumps(val)
                except: obj[key] = self.__np2dict(val)
            return obj
        else : return obj

    def __dict2np(self,obj):
        if isinstance(obj, list): return np.array(obj)
        elif isinstance(obj, dict): 
            for key, val in obj.items():
                obj[key] = self.__dict2np(val)
            return obj
        else : return obj
