print("RUN: main.py")

from machine import Pin
import time

from config import utelegram_config
from config import chat_config

import utelegram

motion = False
muted = False
detections = []


def handle_interrupt(pin):
  global motion
  motion = True
  global int_pin
  int_pin = pin
  

pir = Pin(27, Pin.IN)

pir.irq(trigger = Pin.IRQ_RISING, handler = handle_interrupt)

def getTime():
  current_time = time.localtime()
  return str(current_time)

# setup bot
bot = utelegram.ubot(utelegram_config['token'])

# sends message that informs that command is not recognized
def default_handler(message):
  bot.send(message['message']['chat']['id'], 'Not recognized command. Type /help for list of available commands.')

# sends the contents of help.txt as a message
def help(message):
  f = open('help.txt', 'r')
  fc = f.read()
  f.close()
  bot.send(message['message']['chat']['id'], fc)

# toggle mute on/off
# TODO: pin the mute status message to chat
def mute(message):
  global muted
  if muted:
    muted = False
    bot.send(message['message']['chat']['id'], 'Mute off')
  else:
    muted = True
    bot.send(message['message']['chat']['id'], 'Mute on')
  

# sends stored detections
def list_detections(message):
  bot.send(message['message']['chat']['id'], detections)

# configuring utelegram functions
bot.set_default_handler(default_handler)
bot.register('/mute', mute)
bot.register('/list', list_detections)
bot.register('/help', help)

# saves detections to list. list holds only 10 most recent detections
def add_detection(detection):
  if len(detections) == 10:
    detections.pop(0)
    detections.append(detection)
  else:
    detections.append(detection)


while True:
  bot.read_once()

  if motion:
    # if mute is on, then save to detections, else save to detections and send message
    if muted:
      d = 'MUTED Motion detected at ' + getTime()
      print(d)
      add_detection(d)
    else:
      d = 'Motion detected at' + getTime()
      print(d)
      add_detection(d)

      #the id being used here is the chat_id from telegram
      bot.send(chat_config['id'], d)
    
    motion = False