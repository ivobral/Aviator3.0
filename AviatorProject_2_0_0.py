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
from OpenAviator import AviatorStarter
from PlayingSimulator import WinSimulator
from PlayingSimulator import RealPlaying
from Functions import helpFunctions
import os
from Settings import SetUp

# path do geckodriver-a
s = Service(executable_path="C:\\Users\\petar\\Documents\\GeckoDriver\\geckodriver.exe")

print("Before starting Firefox!!!")
driver = webdriver.Firefox(service= s)                                  #otvara Firefox
driver.get("https://casino.supersport.hr/")                           #dohvaća stranicu

numOfSession = helpFunctions.getSession()                           # dohvaca broj prosle sesije ili 0 ako je prva
logSession = "Number of session: " + str(numOfSession) + '\n'       # ispis u log datoteku
helpFunctions.log(logSession)                                       # ispis u log datoteku

textFilePath = "Results/results" + str(numOfSession) + ".txt"       # text file u koji ce se ispisivati rezultati po principu resultN.txt, gdje je N - broj sesije
f = open(textFilePath, "a+")                                        # stvaranje te datoteke
textTitle = "Session " + str(numOfSession)                          # ispis naslova u resultsN.txt datoteku
f.write(textTitle)                                                  # ispis naslova u resultsN.txt datoteku
f.write('\n')                                                       # ispis naslova u resultsN.txt datoteku

# class that starts Aviator
control = AviatorStarter()
driver = control.startAviator(driver)
print("Aviator start successful!")

# control variables
controlRound = 0                # kontrola runde
roundCounter = 0                # brojac rundi
continueToIf = 0                # kontrolna variabla pojedine runde
firstRoundCheck = 0             # firstRoundCheck - prva runda se ignorira jer se moze desiti da program ne odigra prvu ruku

# text file
f = open("results.txt", "w")
result = ""

# simulator 
gameMode = SetUp.gameMode                        # gameMode = 0 -> simulator, gameMode = 1 -> simulator + stvarno igranje
aviatorMode = SetUp.aviatorMode                  # aviatorMode = 0 -> Demo Aviator, aviatorMode = 1 -> Real Aviator
if gameMode == 0:
    player = WinSimulator()
elif gameMode == 1:
    player = RealPlaying()
else:
    print("Error with gameMode!")
    helpFunctions.log(print)

time.sleep(2)

while(1):

    # blokovi u kojima su pohranjeni rezultati
    while (1):
        try:
            payouts_block = driver.find_element(By.CLASS_NAME, "payouts-block")
            break
        except:
            pass

    history = payouts_block.find_elements(By.TAG_NAME, "div")

    # provjerava je li postoji element ČEKAM IDUĆU RUNDU
    try:
        check = driver.find_element(By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div/app-bet-timer/div/div[2]")
        # nakon analize podataka, "zakljucava" se ulaz u IF dok ne zavrsi naredna runda
        continueToIf += 1
    except NoSuchElementException:
        # blokira ulaz u IF, dok ne zavrsi trenutna runda
        continueToIf = 0
        # otvara ulaz u IF za analizu prethodne runde
        controlRound = 0

    if continueToIf == 1:
        if controlRound == 0:
            roundCounter += 1
            # controlRound se mjenja na 1 koja blokira ponovni ulaz u IF dok trenutna runda ne zavrsi
            controlRound = 1
            result = history[0].text
            # upis rezultata u resultN.txt datoteku
            helpFunctions.writeResultFile(textFilePath, result)
            # simulator
            # ucitavanje rezultate, drivera i varijable koje ce provjeriti prvu rundu
            player.Calculate(float(result[:-1]), driver, firstRoundCheck)
            print(player.getResults(roundCounter, str(result[:-1])))

            # first round check
            if firstRoundCheck == 0:
                firstRoundCheck = 1
                if gameMode ==1:
                    # postavljanje prvog bet i namjestanje buttona
                    # unesi pocetni bet
                    starter = driver.find_element(By.XPATH, player.getInputBetPath())
                    helpFunctions.Input_function(starter, str(SetUp.firstBet))
                    # prebacuje na automatski nacin rada aviatora
                    starter = driver.find_element(By.XPATH, player.getAutomatskiButtonPath())
                    starter.click()
                    # stavlja auto switch na ON
                    starter = driver.find_element(By.XPATH, player.getSwitchAutoPath())
                    starter.click()
                    # postavlja auto isplatu na mult1 iz Setting.py
                    starter = driver.find_element(By.XPATH, player.getAutoIsplataInputPath())
                    helpFunctions.Input_function(starter, str(SetUp.mult1))
                    # stiska Kladi se button
                    starter = driver.find_element(By.XPATH, player.getKladiSeButtonPath())
                    starter.click()
    else:
        pass
f.close()