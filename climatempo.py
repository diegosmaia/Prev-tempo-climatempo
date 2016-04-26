#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################
# Objecto Climatempo - Coleta de dados do site Climatempo
# Filename: climatempo.py
# Revision: 1.0
# Revision_data: 26/04/2016
# Date: 29/03/2016
# Author: Diego Maia - diegosmaia@yahoo.com.br Telegram - @diegosmaia

#######################################################################
# Import
#######################################################################

# https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
try:
    from bs4 import BeautifulSoup  # To get everything
except ImportError:
    from BeautifulSoup import BeautifulSoup

from datetime import datetime
import urllib
import re

from django.utils.encoding import smart_str
import MySQLdb as dbMySQL


########################################################################

class Climatempo(object):

    def __init__(self):

        self.__dbMysqlconnect = None
        self.__dadosextraidos = {}
        self.__cidadenome = None
        self.__dbMysqlconnect_error = None

    def extrairdados(self,site_url,cidadenome):
        self.__cidadenome=cidadenome
        today = datetime.now()
        html = urllib.urlopen(site_url).read()
        soup = BeautifulSoup(html, "lxml")

        extractday = []
        extractmm = []

        for box in soup.findAll('p', {'class': 'left nornal font14 master'}):
            txt = box.text
            extractday.append(txt)

        for i in extractday:
            i = smart_str(i)

        for box in soup.findAll('div', {'class': 'left top20'}):
            txt = box.text
            txt = re.findall('(\d+mm)', txt)
            txt = re.findall('(\d+)', str(txt))
            extractmm.append(txt)

        extractmm = [map(int, x) for x in extractmm]

        total = 0

        for data in xrange(0, len(extractday)):
            txt = re.findall('(\d+/\d+)', str(extractday[data]))
            extractday[data] = txt[0] + '/' + str(today.year)

        for i in xrange(0, len(extractmm)):
            total = sum(extractmm[i], total)

        self.__dadosextraidos = {"datainicio":extractday[0], "datafinal": extractday[9], "totalmm_semana":total, "totalmm_dia": extractmm[0][0]}

    def getdadosextraidos(self):
        return self.__dadosextraidos

    def __MySQLconnect(self,servidor,bancodedados,user,password):

        ##########################################
        # CONEXAO BANDO DE DADOS MYSQL
        # http://blog.mclaughlinsoftware.com/2015/04/12/python-mysql-program/
        ##########################################

        try:
            dbconexao = dbMySQL.connect(servidor, bancodedados, user, password)
            self.__dbMysqlconnect = dbconexao
            return True

        except dbMySQL.Error, e:
            self.__dbMysqlconnect_error = "Error %d: %s" % (e.args[0], e.args[1])
            return False

    def __MySQLdisconnect(self):
        self.__dbMysqlconnect.close()
        self.__dbMysqlconnect = None

    def getMysqlerror(self):
        return self.__dbMysqlconnect_error

    def savetomysql(self,servidor,bancodedados,user,password):

        ##########################################
        # CONEXAO BANDO DE DADOS MYSQL
        # http://blog.mclaughlinsoftware.com/2015/04/12/python-mysql-program/
        ##########################################

        if self.__MySQLconnect(servidor, bancodedados, user, password) == True and self.__cidadenome:

            cur = self.__dbMysqlconnect.cursor()

            #################################
            #  Database Structure - climatempo
            #################################
            # 1 - cod         int(8)
            # 2 - cidade      varchar(40)
            # 3 - previsao    int(4)

            vardbclimatempo_data = (datetime.strptime(self.__dadosextraidos['datainicio'], "%d/%m/%Y")).strftime("%Y/%m/%d")

            sql = "INSERT INTO climatempo(dataprev,cidade,previsao) VALUES('%s','%s','%f')" \
                   % (vardbclimatempo_data, self.__cidadenome, self.__dadosextraidos['totalmm_dia'])
            cur.execute(sql)
            self.__dbMysqlconnect.commit()
            self.__MySQLdisconnect()
            return True
        else:
            return False