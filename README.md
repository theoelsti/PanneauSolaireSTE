# Projet : Panneau solaire

## Site web  
Dossier Codinks/SiteWeb/*
Le script shell `ws.sh` permet de déplacer l'intégralité vers `/var/www/html/panneau/`
## Base sql 
Fichier sql dans `/Codinks/panneau.sql` à importer. 
## Script Python
Le dossier `/Codinks/Prod/*` Contient : 
- Le script Python
- Les pages html des mails

## Config GPIO

Les pins gpio sont modifiables dans le script `Codinks/Prod/script.py`

```python=32
servoPIN = 18
buttonPIN = 6
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
```
Il faut également configurer ses identifiants e-mail 
```python=24
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
piMail = "MAIL-SENDER"
piPassword = "PASSWORD"
myMail = "MAIL-RECEIVER"
```

Les identifiants sql sont également modifiables
```python=11
empty="TRUNCATE TABLE releves;"
DB_SERVER ='localhost' 
DB_USER='root'     
DB_PWD='root'          
DB_BASE='panneau' 
```

### Si vous êtes dans une nouvelle ville, *modifiez l'url d'api ligne **49***