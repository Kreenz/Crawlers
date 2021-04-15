# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:20:11 2020

@author: Antoni
"""
import xlsxwriter
import os
import re

regex = re.compile(r'-?\d+')


info = [];
red = ['Afrutado','Especiado','Joven','Barrica','Ligero','Cuerpo']
white = ['Joven','Barrica','Ligero','Cuerpo','Poco aromático','Muy aromático']
rose = ['Afrutado','Especiado','Ligero','Cuerpo','Pálido','Intenso']
generous = ['Ligero','Cuerpo','Seco','Dulce','Poco complejo','Muy complejo']
sweet = ['Poco complejo','Muy complejo','Poco dulce', 'Muy dulce']
bubbly = ['Seco','Dulce','Afrutado','Cremoso','Crianza corta','Crianza larga']


class IC:

    def _replace_keys(self,wineType,info):
        for index,key in enumerate(wineType):
            info[key] = list((info.pop('var' + str(index+1))).values())[0]
        return info
    def _add_wine(self,info):
        base = []
        for i in range(0,3):
            try:
                keys = info['var' + str(i+1)]
                base.extend(list(keys))
            except KeyError:
                break
        if base == red:
            self.red.append(self._replace_keys(red,info))
        elif base == white:
            self.white.append(self._replace_keys(white,info))
        elif base == rose:
            self.rose.append(self._replace_keys(rose,info))
        elif base == generous:
            self.generous.append(self._replace_keys(generous,info))
        elif base == sweet:
            self.sweet.append(self._replace_keys(sweet,info))
        elif base == bubbly:
            self.bubbly.append(self._replace_keys(bubbly,info))


    def writeHeaders(self):
        print("creating document")
        workbook = xlsxwriter.Workbook("infovinos_{}.xlsx")
        worksheet = workbook.add_worksheet(name='Sheet1')
        cell_format = workbook.add_format({'bold': True, 'bg_color': '#92D050'})
        worksheet.write(0, 0,"nombre",cell_format)
        worksheet.write(0, 1,"origen",cell_format)
        worksheet.write(0, 2,"email",cell_format)
        worksheet.write(0, 3,"telefono",cell_format)

        return workbook, worksheet

    def write_contents(self,worksheet,workbook):
        for index,wine in enumerate(info):
            worksheet.write(index+1, 0,wine["nombre"])
            worksheet.write(index+1, 1,wine["origen"])
            worksheet.write(index+1, 2,wine["email"])
            worksheet.write(index+1, 3,wine["telefono"])
        workbook.close()

    def write_concrete(self):
        # TODO
        a = 2

    def writeLists(self):
        names = ['red','white','rose','generous','sweet''bubbly']
        # Iterate both lists at the same time
        # TODO: potser trobar una millor forma d'estructuarar
        workbook, worksheet = self.writeHeaders()
        self.write_contents(worksheet,workbook)

    def feedSoup(self,soup, correo):
        """
        "Feeds" the soup to be parsed in order to add a wine.
        Parameters
        ----------
        soup : BeautifulSoup
            soup representing a webpage where the info is stored.

        Returns
        -------
        None.

        """
        content = soup.body.find_all("dd");
        info.append({ 'nombre': soup.body.find("big").text if soup.body.find("big").text else "No hi ha", 'email': correo if correo else "No hi ha", 'telefono': content[5].text if content[5].text else "No hi ha", 'origen': content[8].text if content[8].text else "No hi ha"})
        
    def __init__(self):
        self.info = []
        self.red = []
        self.white = []
        self.rose = []
        self.generous = []
        self.sweet = []
        self.bubbly = []
