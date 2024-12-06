import discord, datetime, shutil, requests, random, asyncio, subprocess
import secrets

MonthName = {'01': 'Januar', '02': 'Februar', '03': 'März', '04': 'April', '05': 'Mai', '06': 'Juni', '07': 'Juli', '08': 'August', '09': 'September', '10': 'Oktober', '11': 'November', '12': 'Dezember'}
vuepressImmages = ''
error = ''

print('Month and Year in the following format: 01.2001')
YearMonth = input('Month and Year: ')
YearMonth = YearMonth.split('.')
Month = YearMonth[0]
Year = YearMonth[1]

print('Pulling the repository and creating a picture dir...')
if subprocess.call(['git', 'pull'], cwd='draussenfunker.github.io') != 0:
    exit('Error, can not pull the repository, Exiting')
    pass
if subprocess.call(['mkdir', f'docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/'], cwd='draussenfunker.github.io') != 0:
    #exit('Error, can not create picture dir, Exiting')
    pass
print('Ready')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in')
    
    ImmageCount = 0
    global vuepressImmages
    global error

    channel = client.get_channel(secrets.channelID)
    async for message in channel.history(limit=500, after=datetime.datetime(int(Year), int(Month), 1),): #before=datetime.datetime(int(Year), int(Month) + 1, 1)): <-- dos not work for December 12 + 1 = 13
        if message.attachments != []:
            if message.content == '':
                print('\n\nNo description')
                vuepressImmages += '\n---\n\n'

                line = vuepressImmages.count('\n') + 2
                error += f'No description in line {line}\n'

            else:
                print(f'\n\nDescription: {message.content}')

                # <@614242831434776576> <#1062798608581267636>
                if '<@' in message.content or '<#' in message.content:
                    print('Error: @ or # in message')

                    line = vuepressImmages.count('\n') + 2
                    error += f'@ or # in line {line}\n'                     # Line count dos not work properly

                vuepressImmages += f'\n{message.content}\n\n'

            print(f'\nReaction: {message.reactions}\n')

            for Attatchment in message.attachments:
                print(f'Downloading immage nr. {ImmageCount:02d}')

                ImmageName = f'{ImmageCount:02d}_{Month}-{Year}.jpg'
                LocalPath = f'draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/{ImmageName}'

                shutil.copyfileobj(requests.get(Attatchment.url, stream=True).raw, open(LocalPath, 'wb'))                       # needs to be async and also save .png not as .jpg

                vuepressImmages += f'![Bilder des Monats](/aktivitaeten/BDM-{Year}-{Month}/{ImmageName})\n'
                ImmageCount += 1
    
    print('\n\nClosing Discord')
    await client.close()

client.run(secrets.botToken)

print('\nNumber of tite Immage the following format: 01')
CoverImgNr = input('Title immage: ')
vuepressFileText = f'''---
title: Bilder des Monats {MonthName[Month]} {Year}
description:
    Bilder des Monats {MonthName[Month]} aus unserer Community im Discord.
type: activity
image: /aktivitaeten/BDM-{Year}-{Month}/{CoverImgNr}_{Month}-{Year}.jpg
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

input('Crate commit and push it to the remote repository')
if subprocess.call(['git', 'add', '-A'], cwd='draussenfunker.github.io') != 0:
    Exit('Error, can not add Files to commit')
if subprocess.call(['git', 'commit', '-m', f'\"Bilder des Monats {MonthName[Month]}\"'], cwd='draussenfunker.github.io') != 0:
    Exit('Error, can not commit')
if subprocess.call(['git', 'push'], cwd='draussenfunker.github.io') != 0:
    Exit('Error, can not push the remote Repository')
print('All done, Exiting')
