from pymongo import MongoClient
from datetime import datetime
from datetime import date
from time import sleep
from threading import Thread
import random
import calendar
import pprint

from MyApp.serializers import ChannelSerializer
from MyApp.models import Channel
from . import broker


myclient = MongoClient("mongodb://localhost:27017/")
currentYear = datetime.now().year
database = myclient['Year'+ str(currentYear)]

currentMonth = datetime.now().month


dead=False

class Master:

    flag = 2
    loop = 12
    count = 0
    result = 0
    ans = 0
    msg=0
    def get_time():
        current_time = datetime.now().hour      ##static variable
        static_time = int(current_time) + 1     ##static hour to sleep
        return static_time


    def display():
        global dead
        while (not dead):
            doc=[]
            names=[]
            record={}
            final={}
            global Channel
            for obj in Channel.objects:
                record['channel_Name']=obj.name
                record['channel_unit']=obj.unit
                record['min_Threshold']=obj.minimum
                record['max_threshold']=obj.maximum

            final[obj.name]=record.copy()
            #print(record)

            for num in final:
                if broker.topic==num:
                    col='month'+str(currentMonth)+''+num
                    collection=database[col]
                    collection.insert_one(final[num])
            dead=True



    def days_in_month():
        today = datetime.today().date()
        days_in_current_month = calendar.monthrange(today.year, today.month)[1]
        hours = days_in_current_month * 24
        print(hours)
        return hours


    def message(mqtt):
        for x in mqtt:
            data = x
        user_query = collection.find_one({"channel_Name":  data})
        #pprint.pprint(user_query)

        return user_query

    def query(mqtt): #temp=234

        msg  = Master.message(mqtt)
        current_min=msg["min_Threshold"]
        current_max=msg["max_threshold"]
        current_channel=msg["channel_Name"]

        for x in mqtt:
            data  = x
            thres = mqtt[x]
        if(int(current_min) > int(thres) ):
            query = {"channel_Name": data}
            newvalue =  {"$set": {"comment": "Minimum Threshold crossed"}}
            x = collection.update_one(query, newvalue)
            print(x,"document updated")
            #SAVE

        elif(int(thres) > int(current_max)):
            query = {"channel_Name": data}
            newvalue =  {"$set": {"comment": "Maximum Threshold crossed"}}
            y = collection.update_one(query, newvalue)
            print(y,"documents updated.")

        else:
            query = {"channel_Name": data}
            newvalue =  {"$set": {"comment": "null"}}
            y = collection.update_one(query, newvalue)
            print(y,"documents updated.")



    def month_hour():
        topic=broker.topic
        print(topic)
        thread=Thread(target=Master.display)
        thread.start()
        static_time=Master.get_time()

        """while True:
            current_time=datetime.now().hour
            if(current_time < static_time):
                Master.count = Master.count + 1

            else if(current_time==static_time):
                Thread(target=Master.display).start()
                static_time=static_time+1
                resultt = Master.days_in_month()
                if (Master.count == int(resultt)):
                    Master.result = Master.result + 1
                currentMonth = datetime.now().month
                global database
                collection = database['month'+ str(currentMonth)+''+topic]
                Master.count = 0
            else:
                static_time =static_time + 1

            if (Master.result == int(Master.loop)):
                Master.ans = Master.ans + 1

                currentYear = datetime.now().year
                database = myclient['Year'+ str(currentYear)]
                if (Master.ans == int(Master.flag)):
                    break
           """

