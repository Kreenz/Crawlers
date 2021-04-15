# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 08:56:16 2020

@author: Antoni
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# TODO: migrar de random a numpy.random
import random
from numpy.random import seed
from numpy.random import choice

from multiprocessing.dummy import Pool as ThreadPool

url = 'https://dev.upwine.online'

code = 'S8PMIC'
vin = 'vinalium / vinalium2020'
vin2 = 'cristodelhumilladero / vidrios2020'

def driverChrome():
    return webdriver.Chrome()

def driverFirefox():
    return webdriver.Firefox()

def driverEdge():
    return webdriver.Edge()

def login(driver):
    driver.get(url)
    search_box = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_name('code'))
    search_box.send_keys(code)
    search_box.submit()

def answerInitQuestions(driver,name):
    search_box = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name("rmq-d5822510"))
    search_box.send_keys(name)
    # No es pot guardar en variable ja que un cop modifiquem algo el que tenim guardat no es valid per a modificar
    driver.find_element_by_class_name('rmq-3c20ecb').click()
    driver.find_elements_by_class_name('rmq-3c20ecb')[7].click()
    #driver.find_element_by_class_name('css-xhb3r2').click()
    # Search submit and press
    driver.find_element_by_xpath("//input[@type='submit']").click()
    """
    # Agafem totes les localitats
    search_box = WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_class_name('css-10is79g'))

    # TODO: randomitzar
    # cliquem una
    search_box[0].click()

    # next
    driver.find_element_by_class_name('css-j9zvqh').click()

    # searchbox conte l'array amb opcions d'on has trobat, amb un random podem seleccioanr varies opcions
    search_box = WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_class_name('css-1thazkx'))
    # TODO: randomitzar
    search_box[1].click()


    # next
    driver.find_element_by_class_name('css-1y4d24f').click()

    # Ara tenim 2 objectes, que simbolitzen les dues agrupacins de possibles respostes
    # ¿Cuál es tu consumo de vino? i ¿Cuánto gastas en vino mensualmente?
    # TODO: randomitzar
    search_box = WebDriverWait(driver, 20).until(lambda x: x.find_elements_by_class_name('css-rxan51'))


    # next
    driver.find_element_by_class_name('css-1y4d24f').click()

    # TODO: seleccionar els valors que es vulguin i randomitzar


    # next
    driver.find_element_by_class_name('css-1y4d24f').click()
    """
def startTasting(driver,name):
    """
    Fills all the information before a tasting in order to simulate a human doing it.

    Parameters
    ----------
    driver : Selenium WebDriver
        Driver used to control the instance.

    Returns
    -------
    None.

    """
    login(driver)
    answerInitQuestions(driver,name)

def randomVista(driver,seed=None):
    """
    Randomizes answers in the vista category.
    Currently it does not support leaving blank answers.

    Parameters
    ----------
    driver : Selenium WebDriver
        Driver used to control the instance.
    seed : Int, optional
        seed used to control the randomness. The default is None.

    Returns
    -------
    None.

    """
    random.seed(seed)
    choices = [-100,0,100]
    # Get into vista screen
    WebDriverWait(driver, 30).until(lambda x: x.find_element_by_class_name('rmq-fb687bfe')).click()
    # Slider1
    slider = driver.find_element_by_class_name('css-ki4xuh')
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(random.choice(choices), 0).release().perform()
    # Slider2
    # sliderID changes when clicked, thanks to that we can use the same id and select the second slider
    time.sleep(2) # Sometimes it goes too quick and skips
    slider = driver.find_element_by_class_name('css-ki4xuh')
    move = ActionChains(driver)
    move.click_and_hold(slider).move_by_offset(random.choice(choices), 0).release().perform()

    # Select color
    options = driver.find_elements_by_class_name('css-1go9q17')
    random.choice(options).click()

    # Accept
    driver.find_elements_by_class_name('rmq-30f0a57f')[1].click()

def randomOlfato(driver,seed=None):
    if seed is not None:
        seed(seed)
    random.seed(seed)
    WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_class_name('rmq-fb687bfe'))[1].click()
    # At most we make 21 choices
    for i in range(0,21):
        if choice([0,1], 1,p=[0+(4*float(i)/100),1-(4*float(i)/100)])[0] == 0:
            print('Break at: {0}'.format(i))
            break
        driver.find_element_by_class_name('css-1k7a50m').click()
        # TODO: no es tenen en compte si seleccionem el mateix camp 2 cops
        options = driver.find_elements_by_class_name('css-2md3s6')
        random.choice(options).click()
        # See if we want to dive in and be more specific
        if random.choice([0,1]) == 1:
            driver.find_element_by_class_name('css-jdnxdw').click()
            options2 = driver.find_elements_by_class_name('css-2md3s6')
            choices = [x - len(options) for x in range(len(options),len(options2))]
            options2[random.choice(choices)+len(options)].click()
            if len(driver.find_elements_by_class_name('css-jdnxdw')) > 1 and random.choice([0,1]) == 1:
                # We can go even deeper
                driver.find_elements_by_class_name('css-jdnxdw')[1].click()
                options3 = driver.find_elements_by_class_name('css-2md3s6')
                choices = [x - len(options2) for x in range(len(options2),len(options3))]
                options3[random.choice(choices)+len(options2)].click()
        driver.find_element_by_class_name('css-18egess').click()

    # Now adjust sliders
    sliders = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_class_name('css-hmlcfo'))
    # We may have too many options to just click and drag, so we just send a key
    choices = [Keys.RIGHT,None,Keys.LEFT]
    for i in range(0,len(sliders)):
        command = random.choice(choices)
        if command is None:
            continue
        sliders[i].send_keys(command)
    time.sleep(2)
    driver.find_element_by_class_name('css-rgmyzt').click()


def randomGusto(driver,seed=None):
    """
    Randomizes answers on the Gusto category.
    Currently it does not support leaving blank answers.

    Parameters
    ----------
    driver : Selenium WebDriver
        Driver used to control the instance.
    seed : Int, optional
        seed used to control the randomness. The default is None.

    Returns
    -------
    None.

    """
    random.seed(seed)
    choices = [-100,-50,0,50,100]
    # Get into gusto screen
    WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_class_name('rmq-fb687bfe'))[2].click()
    for i in range(0,4):
        slider = driver.find_element_by_class_name('css-1kno2t0')
        move = ActionChains(driver)
        move.click_and_hold(slider).move_by_offset(random.choice(choices), 0).release().perform()
    # Accept
    driver.find_element_by_class_name('css-rgmyzt').click()

def randomRating(driver,seed=None):
    """
    Randomizes answers on the Rating category.

    Parameters
    ----------
    driver : Selenium WebDriver
        Driver used to control the instance.
    seed : Int, optional
        seed used to control the randomness. The default is None.

    Returns
    -------
    None.

    """
    random.seed(seed)
    choices = [0,1,2,3,4]
    ratings = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_class_name('MuiRating-decimal'))
    ratings[random.choice(choices)].click()
    calidad = driver.find_element_by_xpath("//select[@name='optionlist']")
    options = calidad.find_elements_by_xpath("option")
    random.choice(options).click()

def initiateDrivers(driverf,num,name):
    """
    Creates a number num of drivers of type driverType

    Parameters
    ----------
    driverType : Function
        Type of driver that has to be created.
    num : INTEGER
        number of drivers to be created and instantiated.

    Returns
    -------
    DriverList: List of drivers of length = num and type = driverType.

    """
    drivers = []
    for i in range(1,num+1):
        driver = driverf()
        startTasting(driver,name+str(i))
        drivers.append(driver)
        time.sleep(len(drivers)/6)
        randomVista(driver)
        time.sleep(len(drivers)/6)
        randomGusto(driver)
        time.sleep(len(drivers)/6)
        randomOlfato(driver)
        time.sleep(len(drivers)/6)
        randomRating(driver)
    return drivers

def main(drivers):
    print('before sleep')
    time.sleep(10)
    drivers_flat = [item for sublist in drivers for item in sublist]
    for driver in drivers_flat:
        print('ite')
        driver.quit()



if __name__ == "__main__":
    drivers = []
    # Paralelizing giving problems

    drivers.extend(initiateDrivers(driverFirefox,1,'firefox'))
    drivers.extend(initiateDrivers(driverEdge,1,'edge'))
    drivers.extend(initiateDrivers(driverChrome,1,'chrome'))
    """
    pool = ThreadPool(3)

    drivers = pool.starmap(initiateDrivers,[(driverChrome,10,'chrome'),(driverFirefox,10,'firefox'),(driverEdge,10,'edge')])
    #drivers = pool.starmap(initiateDrivers,[(driverChrome,1,'chrome'),(driverFirefox,1,'firefox'),(driverEdge,1,'edge')])

    pool.close()
    pool.join()
    """
    for driver in drivers:
        driver.quit()
    #main(drivers)