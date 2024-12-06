# Draussenfunker-BilderDesMonats-Bot

## Requirements
You need Python and the libarys [discord.py](https://pypi.org/project/discord.py) and [requests](https://pypi.org/project/requests/). You can install it with pip or apt.  
```pip install discord.py```  
```sudo apt install python3-discord, python3-requests```

## What does the Bot do?
The Bot searches the channel history to the specified date you put in. If it finds a picture it sves it with the description and builds a vuepress document ready to be merged to the Website.

## Modifing it to your own needs
specify ```botToken``` and ```channelID``` in ```secrets.py```.

## State
Fully Working now

## Known Bugs
Timeout while downloading big Picutures. Fix work in progress.
