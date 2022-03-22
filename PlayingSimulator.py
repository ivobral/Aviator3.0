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
from Functions import helpFunctions
import os
from Settings import SetUp

# klasa koja simulira igru 
# koriste se imaginarni bet i balance dok su rezultati stvarni
class WinSimulator(object):
    bet = SetUp.firstBet                   # pocetni bet
    totalBet = SetUp.firstBet              # sluzi za kontrolu sljedeceg bet-a u slucaju koeficjenta < 1.2
    balance = SetUp.balance                # imaginarno stanje
    mult1 = SetUp.mult1                    # izlaz 1
    mult2 = SetUp.mult2                    # izlaz 2
    controlSimulator = 0                   # stanje 0 - koef > 1.2 /// stanje 1 - koef < 1.2, 1 ostaje sve dok ne dode koef > 1.5
    constant = SetUp.firstBet              # sluzi za vracanje pocetnih uvjeta nakon povratka iz stanja 1 u 0
    betHistory = [0, 0]                    # sluzi samo za ispis proslog/sljedeceg beta u message
    drive = 0                              # ucitavanje drivera u nista

    # ucitavanje drivera
    def _init_(self, driver):
        self.drive = driver
 
    # funkcija koja racuna stanje nakon sta je avion odletia
    def Calculate(self, result, driver, firstRoundCheck):
        if firstRoundCheck != 0:
            self.balance = self.balance - self.bet  # oduzimanje bet-a od balance odmah u startu
            self.betHistory[0] = self.bet           # ucitavanje prvog beta - sluzi samo za ispis u message

            # prvi slucaj - koef je <= 1.2 i program ostaje u mogu 0
            if result > 1.2 and self.controlSimulator == 0:
                self.balance = self.balance + self.bet*1.2
                self.betHistory[1] = self.bet

            # drugi slucaj - koef je > 1.2, bet se povecava, a program ide u mod 1
            elif result <= 1.2 and self.controlSimulator == 0:
                self.bet = self.totalBet*2
                self.totalBet = self.totalBet + self.bet
                self.controlSimulator = 1
                self.betHistory[1] = self.bet

            # treci slucaj - program je u modu 1, a koef ide preko 1.5, ulog se vraca na pocetni, a program se vraca u mod 0
            elif result > 1.5 and self.controlSimulator == 1:
                self.balance = self.balance + self.bet*1.5
                self.bet = self.constant
                self.totalBet = self.constant
                self.controlSimulator = 0
                self.betHistory[1] = self.bet

            # cetvrti slucaj - koef je <= 1.5, ulog se povecava opet, a program ostaje u modu 1
            elif result < 1.5 and self.controlSimulator == 1:
                self.bet = self.totalBet*2
                self.totalBet = self.totalBet + self.bet
                self.betHistory[1] = self.bet

            # greska (nemoguce)
            else:
                print("Something strange occured!! khmmmm")

    # ispis rezultata i trenutno stanje -> korsti se za ispis u konzoli i u log.txt datoteci
    def getResults(self, roundCounter, resultText):
        message = str(roundCounter) + ". result:" + str(resultText) + '\n' + "Balance: " + str(self.balance) + "\nLast bet: " + str(self.betHistory[0]) + "\nNext bet: " + str(self.betHistory[1]) + "\ntotalBet: " + str(self.totalBet) + '\n'
        helpFunctions.log(message)
        return message


# klasa za stvarno igranje
class RealPlaying(object):
    bet = SetUp.firstBet               # pocetni bet
    totalBet = SetUp.firstBet          # sluzi za kontrolu sljedeceg bet-a u slucaju koeficjenta < 1.2
    balance = SetUp.balance            # imaginarno stanje
    mult1 = SetUp.mult1                # izlaz 1
    mult2 = SetUp.mult2                # izlaz 2
    controlSimulator = 0               # stanje 0 - koef > 1.2 /// stanje 1 - koef < 1.2, 1 ostaje sve dok ne dode koef > 1.5
    constant = SetUp.firstBet          # sluzi za vracanje pocetnih uvjeta nakon povratka iz stanja 1 u 0
    betHistory = [0, 0]                # ne sluzi nicemu
    drive = 0                          # ucitavanje drivera u nista


    # ucitavanje drivera
    def _init_(self, driver):
        self.drive = driver

 
    # path svih buttona - za stvarno igranje
    kladiSeButtonPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button"
    prekiniButtonPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button"
    automatskiButtonPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]"
    manualButtonPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[1]"
    switchAutoPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[2]/div[2]/div[1]/app-ui-switcher/div"
    autoIsplataInputPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[2]/div[2]/div[2]/div/app-spinner/div/div[1]/input"
    inputBetPath = "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[1]/input"
    
 
    def Calculate(self, result, driver, firstRoundCheck):
        drive = driver
        if firstRoundCheck != 0:
            self.balance = self.balance - self.bet
            self.betHistory[0] = self.bet

            # prvi slucaj - koef je <= 1.2 i program ostaje u mogu 0
            if result > 1.2 and self.controlSimulator == 0:
                self.balance = self.balance + self.bet*1.2
                self.betHistory[1] = self.bet
                
                # ucitavanje KladiSe button, bet ostaje isti
                controller = drive.find_element(By.XPATH, self.kladiSeButtonPath)
                controller.click()

            # drugi slucaj - koef je > 1.2, bet se povecava, a program ide u mod 1
            elif result <= 1.2 and self.controlSimulator == 0:
                self.bet = self.totalBet*2
                self.totalBet = self.totalBet + self.bet
                self.controlSimulator = 1
                self.betHistory[1] = self.bet

                # mode change - auto isplata se postavlja na 1.5, a bet se povecava 
                self.modeChange(str(SetUp.mult2), str(self.bet), drive)
            
            # treci slucaj - program je u modu 1, a koef ide preko 1.5, ulog se vraca na pocetni, a program se vraca u mod 0
            elif result > 1.5 and self.controlSimulator == 1:
                self.balance = self.balance + self.bet*1.5
                self.bet = self.constant
                self.totalBet = self.constant
                self.controlSimulator = 0
                self.betHistory[1] = self.bet

                # mode change - auto isplata se vraca na 1.2, a bet se postavlja na pocetni
                self.modeChange(str(SetUp.mult1), str(self.bet), drive)

            # cetvrti slucaj - koef je <= 1.5, ulog se povecava opet, a program ostaje u modu 1
            elif result < 1.5 and self.controlSimulator == 1:
                self.bet = self.totalBet*2
                self.totalBet = self.totalBet + self.bet
                self.betHistory[1] = self.bet

                # mode change  - auto isplata i dalje ostaje 1.5, a bet se povecava
                self.modeChange(str(SetUp.mult2), str(self.bet), drive)

             # greska (nemoguce)
            else:
                print("Something strange occured!! khmmmm")

    # ispis rezultata i trenutno stanje -> korsti se za ispis u konzoli i u log.txt datoteci
    def getResults(self, roundCounter, resultText):
        message = str(roundCounter) + ". result:" + str(resultText) + '\n' + "Balance: " + str(self.balance) + "\nLast bet: " + str(self.betHistory[0]) + "\nNext bet: " + str(self.betHistory[1]) + "\ntotalBet: " + str(self.totalBet) + '\n'
        helpFunctions.log(message)
        return message

    # GETTER
    def getInputBetPath(self):
        return self.inputBetPath

    # GETTER
    def getKladiSeButtonPath(self):
        return self.kladiSeButtonPath

    # GETTER
    def getSwitchAutoPath(self):
        return self.switchAutoPath
    
    # GETTER
    def getAutomatskiButtonPath(self):
        return self.automatskiButtonPath

    # GETTER
    def getAutoIsplataInputPath(self):
        return self.autoIsplataInputPath

    # GETTER
    def getManualButtonPath(self):
        return self.manualButtonPath

    # GETTER
    def getBet(self):
        return self.bet

    # funckija za promjenu vrijednosti auto isplate i vrijednosti beta u aviatoru
    def modeChange(self, value, bet, driver1):
         driver = driver1
         # promjena auto isplate na 1.2 ili 1.5
         controller = driver.find_element(By.XPATH, self.autoIsplataInputPath)
         helpFunctions.Input_function(controller, value)
         # promjena bet-a
         controller = driver.find_element(By.XPATH, self.inputBetPath)
         helpFunctions.Input_function(controller, bet)
         # klikni kladi se ponovno
         controller = driver.find_element(By.XPATH, self.kladiSeButtonPath)
         controller.click()