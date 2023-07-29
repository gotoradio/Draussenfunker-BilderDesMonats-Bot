from discord.ext import commands
import discord
import datetime
import shutil
import requests

Form = '''title: Bilder des Monats Mai 2023
+ description:
+ Bilder des Monats Mai aus unserer Community im Discord.
+ type: activity
+ image: /aktivitaeten/BDM-2023-05/bilderdesmonats_2023-04_2.jpg
+ features:
+ - FOTOS
+ --- +
+ # Bilder des Monats: Mai 2023 +
+ Ohne viele Worte einige Bilder der Draußenfunker. +
+ DM3KP – Achim:
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_01.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_02.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_03.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_04.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_05.jpg) +
+ DK4HAA – Harm:
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_06.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_07.jpg) +
+ DF9HC – Haiko: DA-0244. 20m SSB mit FT-891, Groundplane. +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_08.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_09.jpg) +
+ ![Bilder des Monats](/aktivitaeten/BDM-2023-05/bilderdesmonats_2023-05_10.jpg) +
'''
DescriptionImmageList = []

Count = 1
YearMonth = input("Month.Year :")
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

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
