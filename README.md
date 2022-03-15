# telegram_event_notifier

A telegram bot which lets you setup notifications for the 42 intra-events

You can access a running bot here: https://t.me/fourtytwo_events_bot

## Table of contents
1. [About](#about)
2. [Requirements](#requirements)
3. [How to use](#howtouse)
4. [Goals](#goals)

## About

This project is a telegram bot that lets your interact with events from the intra.
As I have written this bot in about 3 days as a pyton-beginner my spaghetti-code is probably full of bad practices and
errors. During the project I also realized that my approach is far from perfect and therefore one of my [feature goals](#goals) is
to restructure the project

**features:**
- login with your intra
- setup notifications for events
- delete notifications
- get an icalander event to add to your calander
- no constant authorization needed (refreshes tokens automatically)

## Requirements

The basic python-bot runs in a docker container and therefore only needs docker. If you want to run the bot outside of a container you will
find the requirements in bot/requirements.txt and the source files in bot/src.

But because the bot needs the user to authenticate with oauth2.0 with a code, which is send to the redirect-website via a query-parameters called *code* and telegram-bots only accept query-parameters called *start* or *startgroup*, there's also a nginx server running. 

This nginx server simply redirects the request
to the telegram bot with the parameter *code* asigned to *start*.
To run both containers (nginx-server and python-bot) the project uses docker-compose, but you can also run them seperately as they are not using
a docker-network.

## How to use

Clone the repo:
```bash
git clone https://github.com/JeremieSiller/telegram_event_notifier.git
```
go to the directory telegram_event_notifier and create a *.env* file
```
cd telegram_event_notifier && touch .env
```
add following variables to the .env file:
- TOKEN *the token from your telegrambot* -> text the [bot-father] to create a bot
- UID *uid from your intra app* -> go to the intra -> username -> settings -> api -> register new app
- SECRET *secret from your intra app*
- AUTH_LINK *the full authorization link from your intra app*
- REDIRECT_LINK *the redirect link* -> should be the ip of you server with the port the redir-nginx-sever is listening

change the redirection link in the redir/nginx.conf file to your telegram-bot

start the tool:
```bash
docker-compose up
```

## Goals

As I have already mentioned, I want to restructure the project. The goal is to use classes and smaller functions to make the code more modular and easier adjustable. For now I am also saving all authentication tokens and refresh them about every 20 minutes in a database. I realized that this is not necessary, because I changed my approach during the project. Part of the restructure would be to get rid of the database and just safe the tokens in the temporary storage of the programm.

**future features:**
- logout possibilty
- easier setup of notifications -> 'clickable' - commands without arguements
- give updates when new events occur on the intra - (maybe even if some are removed)
- sign up for events - app needs higher roles that can only be given by bocal

As the goal of this bot was to get notifications on intra-events the *future features* have priority
and the following could be implemented at some point:
- evaluation notification
- other api-requests like blackhole-days

[bot-father]:https://t.me/BotFather
