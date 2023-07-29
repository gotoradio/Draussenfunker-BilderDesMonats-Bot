from discord.ext import commands
import discord, datetime, shutil, requests

YearMonth = input("Month.Year :")
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

print("Run: git clone https://github.com/****/draussenfunker.github.io.git; mkdir draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month))
input("Ready?")

NrToMonthName = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

TopForm = '''
---
title: Bilder des Monats {MonthName} {YearNumber}
description:
    Bilder des Monats {MonthName} aus unserer Community im Discord.
type: activity
image: {CoverImg}
features:
    - FOTOS
---

# Bilder des Monats: {MonthName} {YearNumber}

Ohne viele Worte einige Bilder der Draußenfunker.'''

DescriptionForm='''
{Description}'''

ImgForm='''
![Bilder des Monats]({ImgPath}) '''

client = discord.Client(intents=discord.Intents.all()) #intents=discord.Intents.all() is only sometimes necesary, if you get an error remove it!

@client.event
async def on_ready():
    DescriptionImmageList = []
    Count = 1
    DescriptionOld='esdfghjkkml,l'
    print('We have logged in')
    channel = client.get_channel("****")
    async for message in channel.history(limit=500, after=datetime.datetime(int(Year), int(Month) , 1)):
        AttatchmentList = message.attachments
        for Attatchment in AttatchmentList:
            url = Attatchment.url
            print("Found an Immage")
            imageName = str(Count) + ':' + Month + '.' + Year + '.jpg'
            shutil.copyfileobj(requests.get(url, stream=True).raw, open("draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month) + imageName, 'wb'))
            description = message.content
            print(description)
            Umbennenen = [imageName, description]
            DescriptionImmageList.append(Umbennenen)
            Count += 1
    ToPost = TopForm.format(YearNumber=Year, MonthName=NrToMonthName[int(Month)], CoverImg="K.p.")
    for Current in DescriptionImmageList:
        if(Current[1] != DescriptionOld):
            if(Current[1] != ''):
                ToPost = ToPost + '\n'
            ToPost = ToPost + DescriptionForm.format(Description=Current[1])
        ToPost = ToPost +  ImgForm.format(ImgPath="/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month)+Current[0])
        DescriptionOld = Current[1]
    print("Saving vuepress file...")
    vuepressFile = open("draussenfunker.github.io/docs/aktivitaeten/{YearNr}-{MonthNr}-30-Bilder-Des-Monats-{MonthName}.md".format(YearNr=Year,MonthNr=Month, MonthName=NrToMonthName[int(Month)]),"w")
    vuepressFile.write(ToPost)
    vuepressFile.close()
    print("Run: git add -A; git commit -m \"Bilder des Monats {MonthName}\"; git push".format(MonthName=NrToMonthName[int(Month)]))
    print("End of Job. Exiting...")
    await client.close()
client.run("****")
