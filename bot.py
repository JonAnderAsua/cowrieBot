import json

import requests
import telebot
import subprocess

token = '1604019741:AAGnKUXr7g8iR5LSxboEesu_NP7T4F0N-7s' #Bot-aren token-a

bot = telebot.TeleBot(token) #Bot-a lortu

chat_id = ""

def ipLocation(ip):
    uria = "http://ip-api.com/json/" + ip
    erantzuna = requests.get(uria, allow_redirects=False)
    informazioa = json.loads(erantzuna.content)
    emaitza = informazioa['city'] + " - " + informazioa['country']
    return emaitza

def mezuaBidali(mezua):
    bot.send_message(chat_id, mezua)

def azkenKomandoa():
    i = 1
    komandoa = ""
    while komandoa == "":
        try:
            komandoa = subprocess.check_output('docker logs --tail=' + str(i) + ' busy_lumiere | grep command',shell=True)
            komandoa = komandoa.decode("utf-8")

            # Data
            data = ""
            for j in range(0, 10):
                data = data + komandoa[j]

            # Komandoa
            command = komandoa.split("\"")
            emaitza = ""
            for u in range(1, len(command)):
                emaitza = emaitza + command[u]

            # IP helbidea
            ip = komandoa.split("]")
            ip = ip[0]
            ip = ip.split(",")
            ip = ip[2]

            # Datuak bildu
            kokapena = ipLocation(ip)
            emaitza = "Azkenengo komandoa: " + emaitza + "\n Noiz egin da: " + data + "\n Egin duenaren IP helbidea: " + ip + "\nIP helbidea hiri honetan kokatzen da:" + kokapena
            print(emaitza)
            return emaitza

            break
            # Azkenengo i lerroetan komandorik ez badago errorea ateratzen da, ondorioz errore honen agerpena
            # aprobetzatuko dut if bat bezala erabiltzeko
        except Exception:
            i = i + 1

def azkenLerroa():
    komandoa = subprocess.check_output('docker logs --tail=1 busy_lumiere', shell=True)
    komandoa = komandoa.decode("utf-8")
    gertatutakoa = komandoa.split("]")
    data = ""
    i = 0
    while i < 10:
        data = data + komandoa[i]
        i += 1
    emaitza = "Azkenengo lerroak, " + data + "-(e)an eginda, hurrengoa esaten du" + gertatutakoa[1]
    return emaitza

def listener(mezuak):
    global chat_id
    for i in mezuak:
        print("Sartu da")
        chat_id = i.chat.id
        testua = i.text.lower()

        #Gordetako azken lerroa
        if(testua == 'last line'):
            mezua = azkenLerroa()
            print(mezua)
        #Exekutatutako azken komandoa
        elif(testua == 'last command'):
            mezua = azkenKomandoa()
            print(mezua)
        
        bot.send_message(chat_id,mezua)

bot.set_update_listener(listener)
@bot.message_handler(commands=['kaixo'])
def command_kaixo(mezua):
    chat_id = mezua.chat.id
    bot.send_message(chat_id, "Aupa!")

bot.polling(none_stop=True)
