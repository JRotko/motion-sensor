print("RUN: main.py")

from machine import Pin
import time

from config import utelegram_config
from config import chat_config

import utelegram

motion = False
stop = False
muted = False
detections = []


def handle_interrupt(pin):  #Avoid using print() inside isr
  global motion
  motion = True
  global int_pin
  int_pin = pin
  
led = Pin(4, Pin.OUT)
pir = Pin(27, Pin.IN)

pir.irq(trigger = Pin.IRQ_RISING, handler = handle_interrupt)

def getTime():
  current_time = time.localtime()
  return str(current_time)


bot = utelegram.ubot(utelegram_config['token'])

def default_handler(message):
  bot.send(message['message']['chat']['id'], 'Not recognized command. Type /help for list of available commands.')

def help(message):
  f = open('help.txt', 'r')
  fc = f.read()
  f.close()
  bot.send(message['message']['chat']['id'], fc)


def mute(message):
  global muted
  if muted:
    muted = False
    bot.send(message['message']['chat']['id'], 'Mute off')
  else:
    muted = True
    bot.send(message['message']['chat']['id'], 'Mute on')
  

def quit(message):
  global stop
  stop = True
  
def list_detections(message):
  bot.send(message['message']['chat']['id'], detections)

bot.set_default_handler(default_handler)
bot.register('/mute', mute)
bot.register('/quit', quit)
bot.register('/list', list_detections)
bot.register('/help', help)

def add_detection(detection):
  if len(detections) == 10:
    detections.pop(0)
    detections.append(detection)
  else:
    detections.append(detection)


while True:
  bot.read_once()

  if stop:
    bot.send(chat_config['id'], 'System shutting down')
    break

  if motion:
    if muted:
      d = 'MUTED Motion detected at' + getTime()
      print(d)
      add_detection(d)
    else:
      d = 'Motion detected at' + getTime()
      print(d)
      add_detection(d)
      bot.send(chat_config['id'], d)
    
    motion = False