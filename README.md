# Sourcebans Discord Bot


## Description

A simple dicord bot for getting bans from sourcebans. 
Allows you to get bans based on steamID and player IP, also get steamID based on steam profile link. 
Uses REST API for more secure use.


## Installation


### Webserver

1. Add files to your webserver:
    ```sh
    Add files from `webserver` to your page.
    ```

### Disord BOT

1. Install packages:
    ```sh
    npm i discord.js
   pip install steamid-converter
   pip install -U 'steam[client]'
   pip install Flask
    ```
2. Add your links and token in main.py:
    ```sh
    TOKEN - add your discord token.
   SOURCEBANS - add your link for your sourcebans ("https://your-sourcebans.com/index.php?p=banlist&searchText=")
   WEBSITE - add your link for your website from webserver file ("https://your-website.com/index.php")
    ```


## Commands

1. Get ban by SteamID:
    ```sh
    !getban SteamID
    ```
2. Get ban by IP:
    ```sh
    !getbanip IP
    ```
3. Get SteamID form profile URL:
    ```sh
    !steamid URL
    ```