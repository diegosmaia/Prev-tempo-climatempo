#!/usr/bin/env python 
# -*- coding: utf-8 -*-

##########################################################################
# TempoAgora - Script em Python para coletar dados do site climatempo.com.br com BeautifulSoup e enviar msg pelo telegram
# Filename: tempoagora.py
# Revision: 1.0
# Date: 29/03/2016
# Author: Diego Maia - diegosmaia@yahoo.com.br Telegram - @diegosmaia
# Aproveitei algumas coisas:
# https://gist.githubusercontent.com/fmasanori
# http://blog.rodrigolira.net/category/programacao/
# https://pypi.python.org/pypi/pyTelegramBotAPI/0.2.9
# https://github.com/GabrielRF/Zabbix-Telegram-Notification @GabrielRF
# Obs.: Caso esqueci de alguem, por favor, me chame no Telegram que adiciono
# Cidades interessantes Bacia Rio Mucuri UHE SCLA E PCH MUC: Malacacheta, maravilhas, Aguas Formosa,
# Cidades Interessantes Bacia do Chapecó UHE QQX: Ipuaçú e Abelardo Luz.
# Cidades Interessantes Bacia do Vale do Jauru UHE JAU: Jauru, Indiavaí e Fgueirópolis D'oeste.

##########################################################################
# Install c/ pip do Python
# pip install request
# pip install beautifulsoup4 
# pip install html2text #### nao é necessario
# pip install urllib3
# pip install telebot
# sudo pip install lxml
# sudo pip install telepot --upgrade
# sudo apt-get install libxml2 libxml2-dev
# sudo apt-get install python-lxml
# https://github.com/nickoala/telepot#installation
# pip install --upgrade ndg-httpsclient
# easy_install -U setuptools
##########################################################################

from argparse import ArgumentParser
import re
import urllib3
urllib3.disable_warnings()
import sys  

reload(sys)  
sys.setdefaultencoding('utf-8')

# https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
try:
    from bs4 import BeautifulSoup # To get everything
except ImportError:
	from BeautifulSoup import BeautifulSoup          # For processing HTML
	#from BeautifulSoup import BeautifulStoneSoup     # For processing XML
	#import BeautifulSoup                             # To get everything


# guarantee unicode string
_u = lambda t: t.decode('latin-1', 'replace').decode('utf-8', 'replace') if isinstance(t, str) else t
_uu = lambda *tt: tuple(_u(t) for t in tt) 
# guarantee byte string in UTF8 encoding
_u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, unicode) else t
_uu8 = lambda *tt: tuple(_u8(t) for t in tt)




def fix_unicode_list(data):
	datareturn=[]
	for i in xrange(0, len(data)):
		datareturn.append(_u(data[i]))
	return datareturn


def extrair_dados_site(url):

	html = urllib.urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")


	cidadedia=[]
	cidademm=[]

	for box in soup.findAll('p', {'class':'left nornal font14 master'}):
		txt=box.text
		cidadedia.append(txt)

	cidadedia=fix_unicode_list(cidadedia)

	#for i in xrange(0, len(cidadedia)):
	#	print cidadedia[i]


	for box in soup.findAll('div', {'class':'left top20'}):
		txt=box.text
		txt=re.findall('(\d+mm)',txt)
		txt=re.findall('(\d+)',str(txt))
		cidademm.append(txt)


	cidademm=[map(int, x) for x in cidademm]

	total=0

	for i in xrange(0, len(cidademm)-1):
		#print cidademm[i]
		total= sum(cidademm[i],total)
	#print total
	return([cidadedia[0], cidadedia[9],total])

#SCLA
cidade1=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/1093/nanuque-mg')
cidade2=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/156/malacacheta-mg')
cidade3=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/3848/maravilhas-mg')
cidade4=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/211/aguasformosas-mg')
cidade5=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/3692/crisolita-mg')

#QQX
cidade6=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/2182/ipuacu-sc')
cidade7=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/3412/abelardoluz-sc')

#JAU
cidade8=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/5474/indiavai-mt')
cidade9=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/1174/jauru-mt')
cidade10=extrair_dados_site('http://www.climatempo.com.br/previsao-do-tempo/cidade/5472/figueiropolisdoeste-mt')



VARBRIOMUCURI= "Previsão do tempo para a Bacia do Rio Mucuri \nCidades: Malacacheta, Maravilhas, Águas Formosas, Crisolita, Nanuque\nEntre os dias: %s a %s\nTotal de Chuva.: %smm" %(cidade1[0], cidade2[1],cidade1[2]+cidade2[2]+cidade3[2]+cidade4[2]+cidade5[2])
VARBDOCHAPECO= "Previsão do tempo para a Bacia do Chapecó \nCidades: Ipuaçú, Abelardo Luz \nEntre os dias: %s a %s\nTotal de Chuva.: %smm" %(cidade6[0], cidade6[1],cidade6[2]+cidade7[2])
VARBVALEJAURU= "Previsão do tempo para a Bacia do Vale do Jauru \nCidades: Jauru, Indiavaí, Fgueirópolis D'oeste\nEntre os dias: %s a %s\nTotal de Chuva.: %smm" %(cidade8[0], cidade8[1],cidade8[2]+cidade9[2]+cidade10[2])



###################################
# TELEGRAM 
###################################
# http://www.howtobuildsoftware.com/index.php/how-do/bTnv/python-telegram-sending-photo-from-url-with-telegram-bot
# https://github.com/nickoala/telepot
###################################
import telepot


##################################
# Modificar as variaveis chat_id e token_id verificar o howto http://github.com/diegosmaia/prev-tempo-climatempo/Criando Bot no Telegram.pdf
##################################
chat_id='-57169325'
token_id='161080402:AAGah3HIxM9jUr0NX1WmEKX3cJCv9PyWD58'

##################################

bot = telepot.Bot(token_id)
f = open('qge.png', 'rb')
bot.sendPhoto(chat_id, f)
bot.sendMessage(chat_id,VARBRIOMUCURI)
bot.sendMessage(chat_id,VARBVALEJAURU)
bot.sendMessage(chat_id,VARBDOCHAPECO)
f.close

