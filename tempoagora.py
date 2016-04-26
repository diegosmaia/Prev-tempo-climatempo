#!/usr/bin/env python 
# -*- coding: utf-8 -*-

##########################################################################
# TempoAgora - Script em Python para coletar dados do site
# climatempo.com.br com BeautifulSoup e enviar msg pelo telegram
# Filename: tempoagora.py
# Revision: 1.0
# Date: 26/04/2016
# Author: Diego Maia - diegosmaia@yahoo.com.br Telegram - @diegosmaia
# Aproveitei algumas coisas:
# https://gist.githubusercontent.com/fmasanori
# http://blog.rodrigolira.net/category/programacao/
# https://pypi.python.org/pypi/pyTelegramBotAPI/0.2.9
# https://github.com/GabrielRF/Zabbix-Telegram-Notification @GabrielRF
# Obs.: Caso esqueci de alguem, por favor, me chame no Telegram que adiciono
# Cidades interessantes Bacia Rio Mucuri UHE SCLA E PCH MUC

##########################################################################
# Install c/ pip do Python
# pip install request
# pip install beautifulsoup4
# pip install urllib3
# pip install telebot
# sudo pip install lxml
# sudo pip install telepot --upgrade
# sudo apt-get install libxml2 libxml2-dev
# sudo apt-get install python-lxml
# https://github.com/nickoala/telepot#installation
# pip install --upgrade ndg-httpsclient
# easy_install -U setuptools
# sudo apt-get install python-pip python-dev build-essential 
##########################################################################

from argparse import ArgumentParser
from climatempo import Climatempo
import sys  

reload(sys)  
sys.setdefaultencoding('utf-8')

varBaciaRioMucuri={}
climatempo=Climatempo()

#SCLA

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/1093/nanuque-mg',"Nanuque-MG")
varBaciaRioMucuri["Nanuque"]=climatempo.getdadosextraidos()

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/156/malacacheta-mg',"Malacacheta-MG")
varBaciaRioMucuri["Malacacheta"]=climatempo.getdadosextraidos()

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/3848/maravilhas-mg',"Maravilhas-MG")
varBaciaRioMucuri["Maravilhas"]=climatempo.getdadosextraidos()

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/211/aguasformosas-mg',"AguasFormosas-MG")
varBaciaRioMucuri["AguasFormosas"]=climatempo.getdadosextraidos()

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/3692/crisolita-mg',"Crisolita-MG")
varBaciaRioMucuri["Crisolita"]=climatempo.getdadosextraidos()

climatempo.extrairdados('http://www.climatempo.com.br/previsao-do-tempo/cidade/3355/carloschagas-mg',"CarlosChagas-MG")
varBaciaRioMucuri["CarlosChagas"]=climatempo.getdadosextraidos()

varBaciaRioMucuri_msg= "Previsão do tempo para a Bacia do Rio Mucuri \n" \
			   "Cidades: Malacacheta, Maravilhas, Águas Formosas, " \
			   "Crisolita,Carlos Chagas, Nanuque\nEntre os dias: %s a %s\n" \
			   "Total de Chuva.: %smm"\
			   %(varBaciaRioMucuri["Nanuque"]["datainicio"], varBaciaRioMucuri["Nanuque"]["datafinal"],
				 varBaciaRioMucuri["Malacacheta"]["totalmm_semana"]+
				 varBaciaRioMucuri["Maravilhas"]["totalmm_semana"]+
				 varBaciaRioMucuri["AguasFormosas"]["totalmm_semana"]+
				 varBaciaRioMucuri["Crisolita"]["totalmm_semana"]+
				 varBaciaRioMucuri["CarlosChagas"]["totalmm_semana"])
varPrevDia_msg="Previsão para o dia %s na cidade de Nanuque é de %smm de chuva"\
               %(varBaciaRioMucuri["Nanuque"]["datainicio"],varBaciaRioMucuri["Nanuque"]["totalmm_dia"])


# ###################################
# # TELEGRAM 
# ###################################
# # http://www.howtobuildsoftware.com/index.php/how-do/bTnv/python-telegram-sending-photo-from-url-with-telegram-bot
# # https://github.com/nickoala/telepot
# ###################################
import telepot


# ##################################
# # Modificar as variaveis chat_id e token_id verificar o howto http://github.com/diegosmaia/prev-tempo-climatempo/Criando Bot no Telegram.pdf
# ##################################
chat_id='-57169325'
token_id='161080402:AAGah3HIxM9jUr0NX1WmEKX3cJCv9PyWD58'

# ##################################

bot = telepot.Bot(token_id)
f = open('qge.png', 'rb')
bot.sendPhoto(chat_id, f)
bot.sendMessage(chat_id,varBaciaRioMucuri_msg)
bot.sendMessage(chat_id,varPrevDia_msg)
f.close

