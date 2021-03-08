# Kool libs 😎 #
import time
from datetime import datetime, timedelta, date
import RPi.GPIO as GPIO
import mysql.connector
import smtplib, ssl
import json
import urllib.request
from email.mime.text import MIMEText
# Kool deklarasions 😎 #
empty="TRUNCATE TABLE releves;"
DB_SERVER ='localhost' 
DB_USER='root'     
DB_PWD='root'          
DB_BASE='panneau' 

angle = [
        [0,0,0,0,0,0,0,0,0,35,35,30,25,25,30,30,35,0,0,0,0,0,0,0],#Hiver
        [0,0,0,0,0,0,0,0,35,30,25,20,15,15,15,20,25,30,35,0,0,0,0,0],#Printemps
        [0,0,0,0,0,0,0,35,30,25,20,15,15,15,15,15,15,20,25,30,35,0,0,0],#Ete
        [0,0,0,0,0,0,0,0,35,30,25,20,15,15,15,20,25,30,35,0,0,0,0,0]#Automne
    ]

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
piMail = "MAIL-SENDER"
piPassword = "PASSWORD"
myMail = "MAIL-RECEIVER"

panelState = 1

servoPIN = 18
buttonPIN = 6
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(buttonPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
p = GPIO.PWM(servoPIN, 50)
mode = 0
mailauto = ''
mailmanu = ''
mails = ['mailauto.html','mailmanu.html']
with open(mails[0], 'r') as file:
    mailauto = file.read()
with open(mails[1], 'r') as file:
    mailmanu = file.read()
seuil = 57
actualRaffal = 0
apiurl = "http://www.infoclimat.fr/public-api/gfs/json?_ll=48.9,2.08333&_auth=AxlTRAJ8VHYDLlptBnAAKVc%2FVWAPeQMkBnoHZFs%2BUC0CaFQvBXkHZ1YnUDIPN1ViWGgBYll5ACdWNwZoWzFSOANnUz8CYlQpA3NaJQY3ACtXe1U9DzYDJQZnB2NbPlAtAmBUMAVjB3tWOFA2DzhVflh0AWBZYAA5VjcGYFs0UjkDaVM1AmRUKQNzWj4GNgA1V2NVNw8yAzIGMQdgWzNQZgJkVGMFbgd7VjFQMw8%2BVWZYaAFiWWcAOFYqBn5bT1JCA31TdwIjVGMDKlolBmMAalcw&_c=2af31fc3ffe381b24c464ef727e7049d"
ignore = ["request_state", "request_key", "message", "model_run", "source"]
request_response = {} 
firstSet = False
buttonPressed = False
# Kool foncksion 😎 #
def simp(channel):
    global buttonPressed
    print('clicked')
    buttonPressed = True

def sendMail(template = 0, raffale = 0.00):#0 = 
    server = smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT)
    server.starttls()
    server.login(piMail, piPassword)
    if(template == 0):
        my_email = MIMEText(mailauto, "html")
        my_email["From"] = "alertes@panelshield.gg"
        my_email["To"] = "client@panelshield.gg"
        my_email["Subject"] = "Bulletin d'alerte PanelShield"
        server.sendmail(piMail,myMail, my_email.as_string())
        #message = "On a baissé ton panneau frérot la raffale était trop forte = %s km/h"%raffale
    if(template == 1):
        my_email = MIMEText(mailmanu, "html")
        my_email["From"] = "alertes@panelshield.gg"
        my_email["To"] = "client@panelshield.gg"
        my_email["Subject"] = "Bulletin d'alerte PanelShield"
        server.sendmail(piMail,myMail, my_email.as_string())
        #message= "Oh le sang le vent est trop fort (%s km/h)"%raffale
    #server.sendmail(piMail,myMail, message)
    server.quit()

def empty_base():
    try:
        db = mysql.connector.connect(
            host = DB_SERVER, 
            user = DB_USER, 
            password = DB_PWD, 
            database = DB_BASE) #Connexion
        cursor = db.cursor() #Curseur
        cursor.execute(empty) #On envoie la requete et on ferme
        db.commit()
        db.close()
    except Exception as e:
        print("SQL table reset error" + e)

def query_db(sql):
    try:
        db = mysql.connector.connect(
            host = DB_SERVER, 
            user = DB_USER, 
            password = DB_PWD, 
            database = DB_BASE) #Connexion
        cursor = db.cursor() #Curseur
        cursor.execute(sql) #On envoie la requete et on ferme
        db.commit()
        db.close()
    except Exception as e:
        print("SQL query error" + str(e))

def getFromDB(table):
    try:
        db = mysql.connector.connect(
            host = DB_SERVER, 
            user = DB_USER, 
            password = DB_PWD, 
            database = DB_BASE) #Connexion
        cursor = db.cursor(buffered=True) #Curseur
        query = "SELECT * FROM etats;"
        cursor.execute(query) #On envoie la requete et on ferme
        db.commit()
        result_set = cursor.fetchall()
        global mode
        global current
        for row in result_set:
            mode = row[0]
            current = row[1]
        db.close()
        return[mode, current] 
    except Exception as e:
        print("SQL query error: " + str(e))

def idle(auto=False):
    try:
        for i in range(5):
            global buttonPressed
            global panelState
            if(getFromDB("etats")[0]== 1 and auto == True):
                auto = False
            elif(getFromDB("etats")[0]== 0 and auto == False):
                auto = True
            print("Pressed button : ", buttonPressed)
            if(buttonPressed):
                print("Idling function detected that the button has been pressed")
                buttonPressed = False
                liftDownPanel()
                idle_raf(auto)
                return
            else:
                print("Idle ", i) 
                print("Mode : ", auto)
                if(getFromDB("etats")[1] == 1 and auto == False and getFromDB("etats")[1]!=panelState):
                    print('Le client a demandé à lever le panneau')
                    liftUpPanel()
                    idle(False)
                    return
                if(getFromDB("etats")[1] ==0 and auto == False and getFromDB("etats")[1]!=panelState):
                    print('Le client a demandé à baisser le panneau')
                    liftDownPanel()
                    idle_raf(False)
                    return
                if(getFromDB("etats")[1] == 0 and auto == True and getFromDB("etats")[1]!=panelState):
                    print('Le client a demandé à baisser le panneau')
                    liftDownPanel()
                    idle_raf(True)
                    return
                time.sleep(10)
        routine()
    except Exception as e:
        print("Error during idling: ", e)
        cleanQuit()

def idle_raf(auto=False):
    try:
        for i in range(5):
            global buttonPressed
            global panelState
            if(getFromDB("etats")[0]== 1 and auto == True):
                auto = False
            elif(getFromDB("etats")[0]== 0 and auto == False):
                auto = True
            if(buttonPressed):
                buttonPressed = False
            print("Idle raf ", i)
            print("Mode : ", auto)
            if(getFromDB("etats")[1]== 0 and auto == False and getFromDB("etats")[1]!=panelState):
                print('Le client a demandé à baisser le panneau')
                liftDownPanel()
                idle_raf(False)
                return
            if(getFromDB("etats")[1]== 1 and auto == False and getFromDB("etats")[1]!=panelState):
                print('Le client a demandé à lever le panneau')
                liftUpPanel()
                idle(True)
                return
            if(getFromDB("etats")[1]== 1 and auto == True and getFromDB("etats")[1]!=panelState):# Si le client veut lever le panneau
                print('Le client a demandé à lever le panneau')
                liftUpPanel()
                idle(True)
                return
            time.sleep(10)
        routine()
    except Exception as e:
        print("Error during idle raf : ", e)
        cleanQuit()

def sleepSeason():
    thighs = date.today()
    month = thighs.strftime("%m")
    if(month == "01" or month == "02" or month == "03"):#Hiver
        return 0
    if(month == "04" or month == "05" or month == "06" ):#Printemps
        return 1
    if(month == "07" or month == "08" or month == "09"):#Printemps
        return 2
    if(month == "10" or month == "11" or month == "12"):#Printemps
        return 3

def setAngle(angle):
    duty = int(angle) / 18 + 3
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    p.ChangeDutyCycle(duty)

def liftDownPanel():
    global panelState
    query_db('UPDATE etats SET current = 0;')
    panelState=0
    setAngle(0)
    print('Panneau baissé, nouvelle attente')
    time.sleep(0.5)

def liftUpPanel():
    global panelState
    global angle
    hour = time.strftime("%H")
    upAngle = angle[sleepSeason()][int(hour)]
    if(not upAngle):
        liftDownPanel()
    else:
        query_db('UPDATE etats SET current = 1;')
        panelState=1
        setAngle(upAngle)
        print("Panneau monté, nouvelle attente")
        time.sleep(0.5)

def gpioSetup():
    p.start(2)
    setAngle(35)
    query_db('UPDATE etats SET current = 1;')
    print('Gpio Initialisé, le panneau est levé')

def cleanQuit():
    p.stop()
    GPIO.cleanup()
    return

def getResponse(link = apiurl):
     empty_base()
     try:
          operUrl = urllib.request.urlopen(link)
          if operUrl.getcode() == 200:
               data = operUrl.read()
               jsonData = json.loads(data)
               global request_response
               global firstSet
               firstSet = False
               request_response = jsonData
               for i in jsonData:
                    if i not in ignore and dateRangeChecker(i):
                         if(firstSet is not True):
                              actualRaffal = float(jsonData[i]['vent_rafales']['10m'])
                              firstSet = True
                              print('Prochaines raffales: ', actualRaffal)
                         raffal = float(jsonData[i]['vent_rafales']['10m'])
                         median = float(jsonData[i]['vent_moyen']['10m'])
                         direction = float(jsonData[i]['vent_direction']['10m'])
                         query = """INSERT INTO releves (date, dir, moy, raf) VALUES ('%s','%s','%s','%s');
                                  """ % (i,direction ,median, raffal )
                         query_db(query)
                         #print("Query doggo")
               return actualRaffal
          else:
               print("Error during api request : Code #", operUrl.getcode())
               cleanQuit()
     except Exception as e:
          print("Error during Response/SQL query : " + e)
          cleanQuit()

def timeIn3Hours():
    #print((datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:00:00"))
    in3hours = str((datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:00:00"))
    if(str(in3hours[11:13]) == "23" or str(in3hours[11:13]) == "00"):
         in3hours = str(in3hours[0:11]) + "01" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "02" or str(in3hours[11:13]) == "03"):
         in3hours = str(in3hours[0:11]) + "04" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "05" or str(in3hours[11:13]) == "06"):
         in3hours = str(in3hours[0:11]) + "07" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "08" or str(in3hours[11:13]) == "09"):
         in3hours = str(in3hours[0:11]) + "10" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "11" or str(in3hours[11:13]) == "12"):
         in3hours = str(in3hours[0:11]) + "13" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "14" or str(in3hours[11:13]) == "15"):
         in3hours = str(in3hours[0:11]) + "16" + str(in3hours[14:])
    elif(str(in3hours[11:13]) == "17" or str(in3hours[11:13]) == "18"):
         in3hours = str(in3hours[0:11]) + "19" + str(in3hours[13:])
    elif(str(in3hours[11:13]) == "20" or str(in3hours[11:13]) == "21"):
         in3hours = str(in3hours[0:11]) + "22" + str(in3hours[13:])
    return in3hours
    #1,4,7,10,13,16,19,22

def nowToObj():
     try:
          now = str(datetime.now().strftime("%Y-%m-%d %H:00:00"))
          now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
          return now
     except Exception as e:
          print("Error during nowToObj : " + str(e))
          cleanQuit()

def timeStrToObj(t):
     try:
          return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
     except Exception as e:
          print("Error during timeStrToObj : " + str(e))
          cleanQuit()

def dateRangeChecker(c):
     try:
          d = timeStrToObj(c) - nowToObj()
          if(str(d)[0] == '-'):
               return 0
          else:
               return 1
     except Exception as e:
          print("Error during dateRangeCheck : " + str(e))
          cleanQuit()

def raffaleChecker(r):#1 : manuel | 0 : auto
     try:
          if(r>seuil):
               print('Raffale Superieure au seuil')
               if(getFromDB("etats")[0] == 0):#Auto
                   liftDownPanel()
                   sendMail(0,r)
                   idle_raf(True)
               elif(getFromDB("etats")[0] == 1):#Manuel
                   sendMail(1,r)
                   if panelState:
                       idle(False)
                   else:
                       idle_raf(False)
          elif(r<seuil):
              print('Raffale Inferieure au seuil')
              if(getFromDB("etats")[0] == 0):#Auto
                  liftUpPanel()
                  idle(True)
              elif(getFromDB("etats")[0] == 1):#Manuel
                   idle(False)
     except Exception as e:
          print("Error during raffal checking process : " + str(e))
          cleanQuit()

def routine():
    raffaleChecker(getResponse())

def setup():
    print("Script Démarré")
    gpioSetup()
    routine()

GPIO.add_event_detect(buttonPIN, GPIO.FALLING, callback=simp, bouncetime=5000)
setup()