from discord.ext import commands
import discord, datetime, shutil, requests, random

MonthName = {
    '01': 'Januar',
    '02': 'Februar',
    '03': 'März',
    '04': 'April',
    '05': 'Mai',
    '06': 'Juni',
    '07': 'Juli',
    '08': 'August',
    '09': 'September',
    '10': 'Oktober',
    '11': 'November',
    '12': 'Dezember'
}
vuepressImmages = ''
error = ''

print('Month and Year in the following format: 01.2001')
YearMonth = input('Month and Year: ')
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

print(f'Run: cd draussenfunker.github.io; git pull; mkdir docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/')
input("Ready?")

# intents=discord.Intents.all() is only sometimes necesary, if you get an error remove it!
# ^^^ Later me has no clue what earlier me ment.
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in')
    
    ImmageCount = 0
    global  vuepressImmages
    global error

    channel = client.get_channel(****)
    async for message in channel.history(limit=500, after=datetime.datetime(int(Year), int(Month), 1)):
        if message.attachments != []:
            if message.content == '':
                print('\n\nNo description')
                vuepressImmages += '\n---\n\n'
            else:
                print(f'\n\nDescription: {message.content}')

                if '<@' in message.content or '<#' in message.content:
                    line = vuepressImmages.count('\n') + 2
                    error += f'@ or # in line {line}\n'

                vuepressImmages += f'\n{message.content}\n\n'
                
            print(f'\nReaction: {message.reactions}\n')

            for Attatchment in message.attachments:
                # Download attatched immage into the right Folder with numerated names
                print(f'Immage: {ImmageCount:02d}')
                #imageName = str(Count) + ':' + Month + '.' + Year + '.jpg'
                ImmageName = f'{ImmageCount:02d}:{Month}.{Year}.jpg'
                LocalPath = f'draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/{ImmageName}'
                shutil.copyfileobj(requests.get(Attatchment.url, stream=True).raw, open(LocalPath, 'wb'))

                vuepressImmages += f'![Bilder des Monats](/aktivitaeten/BDM-{Year}-{Month}/{ImmageName})\n'
                ImmageCount += 1
    
    print('\n\nClosing Discord')
    await client.close()

client.run('****')

print('\nNumber of tite Immage the following format: 01')
CoverImgNr = input('Title immage: ')
vuepressFileText = f'''---
title: Bilder des Monats {MonthName[Month]} {Year}
description:
    Bilder des Monats {MonthName[Month]} aus unserer Community im Discord.
type: activity
image: /aktivitaeten/BDM-{Year}-{Month}/{CoverImgNr}:{Month}.{Year}.jpg
features:
    - FOTOS
---

# Bilder des Monats {MonthName[Month]} {Year}

{vuepressImmages}'''

print('\nSaving vuepress file...')
vuepressFileName = f'draussenfunker.github.io/docs/aktivitaeten/{Year}-{Month}-30-Bilder-Des-Monats-{MonthName[Month]}.md'
vuepressFile = open(vuepressFileName, "w")
vuepressFile.write(vuepressFileText)
vuepressFile.close()

if error != '':
    print(f"\nError:")
    print(error)
    input('Hit return to continue')

print(f'Run: cd draussenfunker.github.io; git add -A; git commit -m \"Bilder des Monats {MonthName[Month]}\"; git push')
