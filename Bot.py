from discord.ext import commands
import discord
import datetime
import shutil
import requests

DescriptionImmageList = []

Count = 1
YearMonth = input("Month.Year :")
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

TopForm = '''
title: Bilder des Monats {MonthName} {YearNumber}
+ description:
+ Bilder des Monats {MonthName} aus unserer Community im Discord.
+ type: activity
+ image: {CoverImg}
+ features:
+ - FOTOS
+ --- +
+ # Bilder des Monats: {MonthName} {YearNumber} +
+ Ohne viele Worte einige Bilder der Draußenfunker. +'''.format(YearNumber=Year)#

MiddleForm
'''
+ {Description}
+ ![Bilder des Monats]({ImgPath}) +
'''

client = discord.Client(intents=discord.Intents.all()) #intents=discord.Intents.all() is only sometimes necesary, if you get an error remove it!

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel("****")
    async for message in channel.history(limit=200, after=datetime.datetime(int(Year), int(Month) , 0)):
        try:
            AttatchmentList = message.attachments
        except:
            print("Kein(e) Bild(er) gefunden")
        else:
            global DescriptionImmageList
            global Count
            for Attatchment in AttatchmentList:
                url = Attatchment.url
                print("Bild gefunden")
                imageName = str(Count) + ':' + Month + '.' + Year + '.jpg'
                shutil.copyfileobj(requests.get(url, stream=True).raw, open(imageName, 'wb'))
                description = message.content
                print(description)
                Umbennenen = [imageName, description]
                DescriptionImmageList.append(Umbennenen)
                Count += 1
    print(DescriptionImmageList)
client.run("****")
