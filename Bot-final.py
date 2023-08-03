from discord.ext import commands
import discord, datetime, shutil, requests, random

YearMonth = input("Month.Year :")
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

print("Run:\ngit clone https://github.com/IamBuildDifferent/draussenfunker.github.io.git; mkdir draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month))
input("Ready?")

NrToMonthName = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

TopForm = '''---
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

ImgForm="![Bilder des Monats]({ImgPath})\n"

client = discord.Client(intents=discord.Intents.default()) #intents=discord.Intents.all() is only sometimes necesary, if you get an error remove it!

@client.event
async def on_ready():
    DescriptionImmageList = []
    Count = 1
    DescriptionOld='esdfghjkkml,l'
    ToPost = ""
    print('We have logged in')
    channel = client.get_channel(****)
    async for message in channel.history(limit=500, after=datetime.datetime(int(Year), int(Month) ,1)):
        AttatchmentList = message.attachments
        for Attatchment in AttatchmentList:
            url = Attatchment.url
            print("Found an Immage")
            imageName = str(Count) + ':' + Month + '.' + Year + '.jpg'
            shutil.copyfileobj(requests.get(url, stream=True).raw, open("draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month) + imageName, 'wb'))
            description = message.content
            print(description)
            print(message.reactions)
            if(description != DescriptionOld):
                ToPost += "\n" #Lerzeile für neune Beschribung
                if(description == ''):
                    ToPost += "----------\n" #Wenn keine Beschribung
                elif(description != ''):
                    ToPost += description + '\n' #Beschreibung
            DescriptionOld = description
            ToPost += ImgForm.format(ImgPath="/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month) + imageName) #Bild Hinzufügen
            Count += 1
    ToPost = TopForm.format(YearNumber=Year, MonthName=NrToMonthName[int(Month)], CoverImg="/aktivitaeten/BDM-{YearNr}-{MonthNr}/".format(YearNr=Year, MonthNr=Month) + str(random.randint(1, Count)) + ':' + Month + '.' + Year + '.jpg') + ToPost
    print("Saving vuepress file...")
    vuepressFile = open("draussenfunker.github.io/docs/aktivitaeten/{YearNr}-{MonthNr}-30-Bilder-Des-Monats-{MonthName}.md".format(YearNr=Year,MonthNr=Month, MonthName=NrToMonthName[int(Month)]),"w")
    vuepressFile.write(ToPost)
    vuepressFile.close()
    print("Run:\ngit add -A; git commit -m \"Bilder des Monats {MonthName}\"; git push".format(MonthName=NrToMonthName[int(Month)]))
    print("End of Job. Exiting...")
    await client.close()
client.run("****")
