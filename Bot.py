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
if subprocess.call(['git', 'pull'], cwd='../draussenfunker.github.io') != 0:
    exit('Error, can not pull the repository, Exiting')
    pass
if subprocess.call(['mkdir', f'docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/'], cwd='../draussenfunker.github.io') != 0:
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

    if int(Month) == 12:
        next_month = datetime.datetime(int(Year) + 1, 1, 1)
    else:
        next_month = datetime.datetime(int(Year), int(Month) + 1, 1)

    async for message in channel.history(limit=500, after=datetime.datetime(int(Year), int(Month), 1), before=next_month):
        if message.attachments != []:
            text = message.content
            skip = False

            for i in message.reactions:
                async for user in i.users():
                    #if user == "techi2":
                    print(user.id)
                    print(i.emoji)

                    if user.id == secrets.myUserID:
                        if '✖' in i.emoji:
                            print('gelöscht')
                            skip = True

                        if '⬆️' in i.emoji:
                            text = text_prev

                        if '⬇️' in i.emoji:
                            async for message_next in channel.history(limit=1, after=message):
                                text = message_next.content

            print(f'\n\nDescription: {text}')

            if not skip:
                if '<@' in text or '<#' in text:
                    print(f'\nError: @ or # in text https://discord.com/channels/{secrets.serverID}/{secrets.channelID}/{message.id}')

                    corrected_text = input('\nCorrected Text, leave empty to skip the picture(s): ')

                    if corrected_text:
                        text = corrected_text
                    else:
                        continue

                vuepressImmages += f'\n{text}\n\n'

                for Attatchment in message.attachments:
                    print(f'Downloading immage nr. {ImmageCount:02d}')

                    ImmageName = f'{ImmageCount:02d}_{Month}-{Year}.jpg'
                    LocalPath = f'../draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/{ImmageName}'

                    shutil.copyfileobj(requests.get(Attatchment.url, stream=True).raw, open(LocalPath, 'wb'))                       # needs to be async and also save .png not as .jpg

                    vuepressImmages += f'![Bilder des Monats](/aktivitaeten/BDM-{Year}-{Month}/{ImmageName})\n'
                    ImmageCount += 1

        text_prev = message.content
    
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

if subprocess.call(['../../../../../../bot/optimize.sh'], cwd=f'../draussenfunker.github.io/docs/.vuepress/public/aktivitaeten/BDM-{Year}-{Month}/') != 0:
    Exit('Error, can not rezise Immages')

print('\nSaving vuepress file...')
vuepressFileName = f'../draussenfunker.github.io/docs/aktivitaeten/{Year}-{Month}-30-Bilder-Des-Monats-{MonthName[Month]}.md'
vuepressFile = open(vuepressFileName, "w")
vuepressFile.write(vuepressFileText)
vuepressFile.close()

if error != '':
    print(f"\nError:")
    print(error)
    input('Hit return to continue')

input('Crate commit and push it to the remote repository')
if subprocess.call(['git', 'add', '-A'], cwd='../draussenfunker.github.io') != 0:
    Exit('Error, can not add Files to commit')
if subprocess.call(['git', 'commit', '-m', f'\"Bilder des Monats {MonthName[Month]}\"'], cwd='../draussenfunker.github.io') != 0:
    Exit('Error, can not commit')
if subprocess.call(['git', 'push'], cwd='../draussenfunker.github.io') != 0:
    Exit('Error, can not push the remote Repository')
print('All done, Exiting')
