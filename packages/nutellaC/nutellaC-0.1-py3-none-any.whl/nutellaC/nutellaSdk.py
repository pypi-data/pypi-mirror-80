import threading
import psutil
import time
import schedule
import asyncio
import base64
from asyncio import Future
import struct
from rx import interval
from apscheduler.schedulers.background import BackgroundScheduler
from nutellaC import nutellaRequests

class Nutella(threading.Thread):

    def __init__(self):
        self.requestData=dict()
        self.psValue=psutil.Process()


    def init(self,modelName=None, projectKey=None, reinit=False):
        self.requestData["projectKey"]=projectKey
        self.requestData["modelName"] =modelName
        self.requestData["reinit"] = reinit


    def config(self,**configDatas):
        for key,value in configDatas.items():
            self.requestData[key]=value

    def log(self,accuracy=None, loss=None,precision=None, recall=None):
        self.requestData["accuracy"]=accuracy
        self.requestData["loss"]=loss
        self.requestData["precision"]=precision
        self.recall["recall"]=recall

    def hardwareSystemValue(self):
        p = psutil.Process()
        self.requestData["cpu"]=min(65535, int(((p.cpu_percent(interval=None) / 100) / psutil.cpu_count(False)) * 65535))
        self.requestData["memory"]= min(65535, int((p.memory_percent() / 100) * 65535))
        self.requestData["net"]=psutil.net_io_counters()
        self.requestData["disk"]=psutil.disk_io_counters()

    def printDict(self):
        print(self.requestData)
        a=nutellaRequests.Requests()
        asyncio.run(a.requestAction(requestDatas=self.requestData))

