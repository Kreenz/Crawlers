# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:20:11 2020

@author: Antoni
"""
import xlsxwriter
import os
import re

regex = re.compile(r'-?\d+')

red = ['Afrutado','Especiado','Joven','Barrica','Ligero','Cuerpo']
white = ['Joven','Barrica','Ligero','Cuerpo','Poco aromático','Muy aromático']
rose = ['Afrutado','Especiado','Ligero','Cuerpo','Pálido','Intenso']
generous = ['Ligero','Cuerpo','Seco','Dulce','Poco complejo','Muy complejo']
sweet = ['Poco complejo','Muy complejo','Poco dulce', 'Muy dulce']
bubbly = ['Seco','Dulce','Afrutado','Cremoso','Crianza corta','Crianza larga']


class DC:



    def _replace_keys(self,wineType,info):
        for index,key in enumerate(wineType):
            info[key] = list((info.pop('var' + str(index+1))).values())[0]
        return info
    def _add_wine(self,info):
        base = []
        for i in range(0,6):
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


    def writeHeaders(self,wine,name):
        workbook = xlsxwriter.Workbook("decantalo_{}.xlsx".format(name))
        worksheet = workbook.add_worksheet(name='Sheet1')
        cell_format = workbook.add_format({'bold': True, 'bg_color': '#92D050'})
        worksheet.write(0, 0,"name",cell_format)
        worksheet.write(0, 1,"description",cell_format)
        worksheet.write(0, 2,"header",cell_format)
        worksheet.write(0, 3,"allergens",cell_format)
        worksheet.write(0, 4,"cellar",cell_format)
        worksheet.write(0, 5,"graduation",cell_format)
        worksheet.write(0, 6,"grapeTypes",cell_format)
        worksheet.write(0, 7,"originName",cell_format)
        worksheet.write(0, 8,"pairing",cell_format)
        worksheet.write(0, 9,"parkerPoints",cell_format)
        worksheet.write(0, 10,"price",cell_format)
        worksheet.write(0, 11,"service",cell_format)
        worksheet.write(0, 12,"volume",cell_format)
        worksheet.write(0, 13,"year",cell_format)
        worksheet.write(0, 14,"originRegion",cell_format)
        col = 15
        for index,value in enumerate(wine):
             worksheet.write(0, col,value,cell_format)
             col += 1
        worksheet.write(0, col,"image",cell_format)

        return workbook, worksheet

    def write_contents(self,wines,names,worksheet,workbook):
        for index,info in enumerate(wines):
            worksheet.write(index+1, 0,info["name"])
            worksheet.write(index+1, 1,info["description"])
            worksheet.write(index+1, 2,info["header"])
            worksheet.write(index+1, 3,info["allergens"])
            worksheet.write(index+1, 4,info["cellar"])
            worksheet.write(index+1, 5,info["graduation"])
            worksheet.write(index+1, 6,info["grapeTypes"])
            worksheet.write(index+1, 7,info["originName"])
            worksheet.write(index+1, 8,info["pairing"])
            worksheet.write(index+1, 9,info["parkerPoints"])
            worksheet.write(index+1, 10,info["price"])
            worksheet.write(index+1, 11,info["service"])
            worksheet.write(index+1, 12,info["volume"])
            worksheet.write(index+1, 13,info["year"])
            worksheet.write(index+1, 14,info["originRegion"])
            col = 15
            for name in names:
                worksheet.write(index+1, col,info[name])
                col += 1
            worksheet.write(index+1, col,info["image"])
        workbook.close()

    def write_concrete(self):
        # TODO
        a = 2

    def writeLists(self):
        names = ['red','white','rose','generous','sweet''bubbly']
        # Iterate both lists at the same time
        for name in names:
            if os.path.exists("decantalo_{}.xlsx".format(name)):
                os.remove("decantalo_{}.xlsx".format(name))
        # TODO: potser trobar una millor forma d'estructuarar
        workbook, worksheet = self.writeHeaders(red,'red')
        self.write_contents(self.red,red,worksheet,workbook)
        workbook, worksheet = self.writeHeaders(white,'white')
        self.write_contents(self.white,white,worksheet,workbook)
        workbook, worksheet = self.writeHeaders(rose,'rose')
        self.write_contents(self.rose,rose,worksheet,workbook)
        workbook, worksheet = self.writeHeaders(generous,'generous')
        self.write_contents(self.generous,generous,worksheet,workbook)
        workbook, worksheet = self.writeHeaders(sweet,'sweet')
        self.write_contents(self.sweet,sweet,worksheet,workbook)
        workbook, worksheet = self.writeHeaders(bubbly,'bubbly')
        self.write_contents(self.bubbly,bubbly,worksheet,workbook)



    def feedSoup(self,soup):
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
        parser = soup.body.find_all("div",class_="col-md-12 col-xs-12 feature-product nopadding")
        info = {'header' : parser[0].text}
        try:
            info['description'] =  soup.body.find("h4",class_="block-head-line nopadding-left col-xs-12").text
        except AttributeError:
            info['description'] = "Na"
        info['name'] = soup.body.find_all("div", class_="page-heading")[1].text.strip()
        # self.info['Origin'] = parser[1].find_all("span")[2].text
        info['cellar'] = parser[2].text.split(":")[1].strip()
        info["originRegion"] = parser[1].text.split(":")[1].strip()
        try:
            info['grapeTypes'] = soup.body.find("div",class_="col-md-12 col-xs-12 feature-product nopadding variedad").text.split(":")[1].strip()
        except AttributeError:
            info['grapeTypes'] = "Na"
        info['originName'] = soup.body.find("div", class_="col-md-12 col-xs-12 feature-product supplier nopadding").text.split(":")[1].strip()
        aux = soup.body.find("div",class_="col-md-12 col-xs-12 feature-product nopadding capacidad").text.split(":")[1].strip().split(" ")[0]
        aux = float("0." + aux.replace(',',''))
        info['volume'] = aux
        info['graduation'] = soup.body.find("div",class_="col-md-12 feature-product nopadding").text.split(":")[1].strip()
        """
        TODO: S'ha d'ajustar la puntuacio que ens donen de les caracteristiques dels vins a les nostres
        """
        scores_fig = soup.body.find_all("div",class_="col-xs-12 col-sm-4 col-md-3")
        for index,score in enumerate(scores_fig):
            spans = score.find_all("span")
            #Depenent de quina posicio de l'array estigui "css-shapes selected" sabem quin es el bo
            name1 =  spans[0].text.strip()
            name2 = spans[2].text.strip()
            divs = spans[1].find_all("div")
            num = 0
            for num,div in enumerate(divs):
                if len(div.get("class")) == 2:
                    break
            num = round(num/9 *10)
            info['var' + str(1+index*2)] = {name1:num}
            info['var' + str((1+index)*2)] = {name2:10-num}



        info['price'] = "Na"
        info['iva'] = "Na"
        #si no hi ha stock no es pot agafar preu
        try:
            aux = soup.body.find("span",class_="price product-price")
            cost = aux.text.split("€")[0].strip()
            info['price'] = float(cost.replace(",","."))
            info['iva'] = not aux.find("span",class_="tax_literal").text is ''
        except Exception:
            print("No preu")
            print(info['name'])
        try:
            info['service'] = soup.body.find("span",class_="temperature").text
        except Exception:
            info['service'] = 'Na'
        try:
            info['allergens'] = soup.body.find("div",class_="grados col-xs-9").find("strong").text
        except Exception:
            info['allergens'] = 'Na'
        try:
            info['pairing'] = soup.body.find("div",class_="maridaje col-xs-9").find("div",class_="recommendation").text.strip()
        except Exception:
            info['pairing'] = 'Na'
        info['parkerPoints'] = "Na"
        info['peñin'] = "Na"
        scorers = soup.body.find_all("li",class_="score")
        for scorer in scorers:
            if "Parker" in scorer.text:
                 value = scorer.text.split("Parker")[1].strip()
                 info['parkerPoints'] = abs(int(regex.findall(string = value)[0]))
                 break
        # Tecnicament el primer que trobem es el de la fitxa de preus de l'ultim any
        info['year'] = soup.body.find("li", class_="active").text.strip()
        info['image'] = soup.body.find(id="thumbs_list_frame").a.get("href")

        self._add_wine(info)

    def __init__(self):
        self.red = []
        self.white = []
        self.rose = []
        self.generous = []
        self.sweet = []
        self.bubbly = []
