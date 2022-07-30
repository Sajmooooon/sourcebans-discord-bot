"""
Author: https://replit.com/@Gargle/MinerMends-247-Discordpy-Tutorial#main.py
Program to keep the bot alive.
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "I am alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()