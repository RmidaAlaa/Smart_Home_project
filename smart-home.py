###Importation de les bibliotheques nécessaire###
import time, datetime
import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop
import os
import pygame, sys
from subprocess import call
now = datetime.datetime.now()
####### Configuration des Pin IN/outs:
###Configuration GPIO######
boutt = 14
led1 = 2 
led2 = 3
led3 = 4
buzzer=23 
gaz=24 
dht=17 
servo = 27
GPIO.setmode(GPIO.BCM)   ##les GPIO fonctionne sous le mode BCM##
GPIO.setup(servo , GPIO.OUT) 
P=GPIO.PWM(27 , 50)
P.start(7.5)
GPIO.setup(dht, GPIO.IN)
GPIO.setup(gaz, GPIO.IN)
GPIO.setup(led1, GPIO.OUT)
GPIO.output(led1, 0)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.output(led2, 0)
GPIO.setup(led3, GPIO.OUT)
GPIO.output(led3,0)
GPIO.setup(14, GPIO.IN , pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
##########################Définition des fonctions :
################fonction de déctection par boutton 
def prebutt():
    telegram_bot.sendMessage (chat_id, str("detection mode activated Sir"))
    while True():
        boutt_state=GPIO.input(14)
        if boutt_state == True:
            GPIO.output(buzzer , HIGHT)
            telegram_bot.sendMessage (chat_id , str("warning !!!!!! some one in the room ")) 
            telegram_bot.sendMessage(chat_id,open('11.jpg ','rb')) 
            time.sleep(3)
            P.ChangeDutyCycle(12.5) #180 degreé
 ###############fonction pour  capteurer un image a partir d’un camera USB:         
def captur():
    call(["fswebcam","-d","/dev/vide0","-r","640*480","--no-banner","./11.jpg"])
###############fonction de detection d'un fuit de gaz 
def presence_gaz():
    try:
        time.sleep(3)
        if GPIO.input(24): 
           GPIO.output(23,True)
           telegram_bot.sendMessage(chat_id,str("Attention!!!!, il ya un fuit de Gaz"))
           GPIO.output(led3,True)
           GPIO.output(buzzer , True)
         else GPIO.output(led3,True):
              time.sleep(1)
              GPIO.output(led3, False)
              time.sleep(1)
             
                GPIO.output(23,False)
                time.sleep(5)
            time.sleep(0.5)
    except:
        GPIO.cleanup()
###################fonction pour activé l'alarme
def Buzzer_on():
    while True:
        GPIO.output(buzzer,GPIO.HIGHT)
        print("beep..")
        time.sleep(5)
  fonction de désactivation de l'alarme
def Buzzer_off():
    while True:
        GPIO.output(buzzer,GPIO.LOW)
        print("STOP beep")
        time.sleep(5)
#######################fonction de musure la températeur et l'humidité##
def temp_hum ():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(11,4)
       yield (humidity) 
       yield (temperature) 
        print ('Temp:{0:0.1}C Humidity {1:0.1}%'.format(temperature,humidity))
        telegram_bot.sendMessage(chat_id,str("Temper:{0:0.1} C Humidity: {1:0.1 f} %"))
fonction de l'ouverture de la porte :
 def Opservo_moteur ():
    try:
        while True:
                P.ChangeDutyCycle(2.5) #0 degreé:opened   
                time.sleep(3)
    except KeyboardInterrupt :
        P.stop()
        GPIO.cleanup()
##################fonction de fermeture de la porte :
def Clservo_moteur ():
    try:
       while True:
                P.ChangeDutyCycle(12.5) ##180 degreé:closed 
                time.sleep(3)
    except KeyboardInterrupt :
        P.stop()
        GPIO.cleanup()    ##rénitialisation##   
#############################identification des commandes avec le Telegram Mobile par l’utilisateur :
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print ('Received: %s' % command)
    print (chat_id )
    if command =='Hi':
        telegram_bot.sendMessage(chat_id,str("Hello ALA :) ")+str("how are you ? can i help you ;)"))
    elif command =='Yes':
        telegram_bot.sendMessage(chat_id,str("for my pleasure:)")+str("how ? "))
    elif command =='Time':
        telegram_bot.sendMessage(chat_id,str(now.hour)+str(":")+str(now.minute))
    elif command =='Weather':
        temp_hum () 
        telegram_bot.sendMessage(chat_id,str("for today we have : Temper:{0:0.1} C Humidity: {1:0.1 f} %"))
    elif command =='Run music':
        telegram_bot.sendMessage(chat_id,str("listen up have fun "))
        telegram_bot.sendMessage(chat_id,open("/home/pi/Downloads"))   
    if command == ‘capture’  ##l’envoie de l’image ##
       captur()
        message ="capture"
       print (‘recieved:%s’ %command)
      message = “capture”
     telegram_bot.sendPhoto(chat_id,open(‘11.jpg’,”rb’))
     message = message +”capture”
     telegram_bot.sendMessage (chat_id, message)
    if 'Open' in command:
        message = "open the door "
        Opservo_moteur ()
        time.sleep(3)
        telegram_bot.sendMessage(chat_id,str("the door was opened"))
     ####activation des differents actionneurs###
    if 'on' in command:
        message = "Turned on "
        if 'led1' in command:
            message = message + "led1" ##led1 activée
            GPIO.output(led1, 1)
        if 'led2' in command:
            message = message + "led2 " ##led2 activée
            GPIO.output(led2, 1)
        if 'buzzer' in command:
            def Buzzer_on()
            message = message + "buzzer" ##L’activation de l’alarme##
            time.sleep(5)
            telegram_bot.sendMessage(chat_id,str("warnings!!!"))
        if 'Motor' in command:
            message = message + "Motor " #activation le ventilateur pour climatiser la chambre#
            GPIO.output(Motor, 1)
       if ' servo' in command:
            message = message + "servo" ## l’ouverture de la porte##
            GPIO.output(servo,1)
        if 'all' in command:
            message = message + "all " ##l’ouverture de tous##
            GPIO.output(led1, 1)
            GPIO.output(led2, 1)
            GPIO.output(buzzer,GPIO.HIGH)
            message = message + "light(s) are opened Sir" ##message envoiée vers Telegram#
        telegram_bot.sendMessage (chat_id, message)
    if 'Close' in command: 
        message = "close the door" ##la fermeture de la porte ##
        Clservo_moteur ()   ## faire un angle 180 degreés ##
        time.sleep(3) 
        telegram_bot.sendMessage(chat_id,str("the door was closed"))
###desactivation des differents actionneurs###
    if 'off' in command:
        message = "Turned off "
        if 'led2' in command:
            message = message + "led2 "
            GPIO.output(led2, 0)
        if 'led1' in command:
            message = message + "led1 "
            GPIO.output(led1, 0)
         if 'buzzer' in command:
            def Buzzer_off()
            message = message + "buzzer "     ##désactivation de l’alarme##
            time.sleep(5)
            telegram_bot.sendMessage(chat_id,str("stop warnings:)"))
        if 'Motor' in command:
            message = message + "Motor "
            GPIO.output(Motor, 0)
        if 'servo' in command:
            message = message +"servo"
            GPIO.output(servo,0)
        if 'all' in command:
            message = message + "all "
            GPIO.output(led2, 0)
            GPIO.output(led1, 0)
            GPIO.output(buzzer, 0)
            message = message + "light(s)"
        telegram_bot.sendMessage (chat_id, message)

####Paramétrage de Bot####

telegram_bot = telepot.Bot('copy your telegram token here ')
print (telegram_bot.getMe())
print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
print('Up and Running....')
telegram_bot.sendMessage ('your -ID- ', "up and running....")
while 1:
   time.sleep(10)    
