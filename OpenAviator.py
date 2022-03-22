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
from Settings import SetUp

# klasa koja sluzi za pokretanje aviatora
class AviatorStarter(object):

    # path za svaki pojedini button
    prijavaPath = "//*[@id='loginButton']"
    nadimakPath = "/html/body/div[4]/div/div[3]/div[2]/div[1]/form/input[1]"
    lozinkaPath = "/html/body/div[4]/div/div[3]/div[2]/div[1]/form/input[2]"
    korisnickoIme = "Dome34"
    lozinka = "JakaLozinka123."
    prijaviSeButtonPath = "/html/body/div[4]/div/div[3]/div[2]/div[2]/button"
    findAviatorInputPath = "/html/body/div[7]/div/div[2]/div[2]/div/input"
    touchAviatorPath = "/html/body/div[7]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]"
    startAviatorPath = "/html/body/div[7]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/div/button[1]"
    startAviatorDemoPath = "/html/body/div[7]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div/div/div/button[2]"
    iFrame = "/html/body/div[12]/div/div[5]/iframe"
    startAviator = ""
    stanjeRacunaPath = "/html/body/div[4]/div/div[3]/div[1]/div[3]/div[1]/div[2]"
    nastaviUIgruPath = "/html/body/div[11]/div/div[2]/div/a[3]"

    # bzvz tu stoji, valjda ne triba
    def _init_(self):
        pass
        
    # funkcija koja pokrece aviator
    def startAviator(self, drive):

        print("Entering startAviator()")
        # Demo/Real aviator
        if SetUp.aviatorMode == 0:
            self.startAviator = self.startAviatorDemoPath
            print("Starting Demo Aviator...")
        elif SetUp.aviatorMode == 1:
            self.startAviator = self.startAviatorPath
            print("Starting Real Aviator...")
        else:
            print("Error while choosing Demo/Real Aviator!")

        # controller - varijabla za sve buttone
        # clicking PRIJAVA button
        controller = drive.find_element(By.XPATH, self.prijavaPath)
        controller.click()

        # entering username
        controller = drive.find_element(By.XPATH, self.nadimakPath)
        controller.send_keys(self.korisnickoIme)
        
        # entering password
        controller = drive.find_element(By.XPATH, self.lozinkaPath)
        controller.send_keys(self.lozinka)
        
        # login
        controller = drive.find_element(By.XPATH, self.prijaviSeButtonPath)
        controller.click()
        print("Logging in!")
        
        # search for aviator frame
        controller = drive.find_element(By.XPATH, self.findAviatorInputPath)
        controller.send_keys("aviator")

        print("Login successful!")
        
        # scrolling down to see aviator
        drive.execute_script("window.scrollTo(0, 500)")
        
        # in order to load everything, waiting 4 seconds
        time.sleep(4)

        # touch aviator pic and "keep finger on it" 
        touchAviator = drive.find_element(By.XPATH, self.touchAviatorPath)
        action = ActionChains(drive)
        action.click_and_hold(on_element = touchAviator)
        action.perform()

        # start Aviator finally
        controller = drive.find_element(By.XPATH, self.startAviator)
        controller.click()

        # provjera je li casino stanje == 0,00
        # ako je tada je pri pokretanju aviatora potrebno kliknuti na "Nastavi u igru" u dijaloskom okviru
        #controller = drive.find_element(By.XPATH, self.stanjeRacunaPath)
        #if SetUp.aviatorMode == 1 and controller.text == "0,00":
        #    controller = drive.find_element(By.XPATH, self.nastaviUIgruPath)
        #   controller.click()

        # waiting until Aviator is loaded
        time.sleep(4)

        # get frame where aviator is located
        controller = drive.find_element(By.XPATH, self.iFrame)

        # switching driver to iFrame
        drive.switch_to.frame(controller)
        
        print("Aviator started successfuly and switched to Aviator frame!")

        time.sleep(1)

        # vraca driver kako bi prenijeli stanje drivera u glavni dio programa
        return drive