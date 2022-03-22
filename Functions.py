import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# neke pomocne funkcije radi preglednosti glavnog koda
class helpFunctions:

    # pohrana broja sesije
    def getSession():
        f = open('data.txt', 'r+')
        lines = f.readlines()
        numOfSession = int(lines[0]) + 1
        f.truncate(0)
        f.seek(0)
        f.write(str(numOfSession))
        return numOfSession

    # ispis u log.txt datoteku
    def log(txt):
        f = open('log.txt', 'a')
        text = txt + '\n'
        f.write(text)
    
    # ispis rezultata u resultN.txt file koji se nalazi u datoteci Results/resultsN.txt - gdje je N - broj sesije
    def writeResultFile(path, result):
        with open(path,"a+") as file:
                file.write(result[:-1])
                file.write('\n')

    # funkcija za unos string vrijednosti u neki web element
    def Input_function(target_input, value):
        target_input.send_keys(Keys.CONTROL + "a")
        target_input.send_keys(Keys.DELETE)
        target_input.send_keys(value)