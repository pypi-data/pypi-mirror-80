from selenium import webdriver
from time import sleep
import schedule
import datetime
import requests

class MetarSpeciTaf:
    def __init__(self, chrome_driver='', line_token='', time_stop=''):
        self.metarspeci_target = "https://nsweb.tmd.go.th/#showMetars"
        self.taf_target = "https://nsweb.tmd.go.th/#showTAFs"
        self.chrome_driver = chrome_driver
        self.line_token = line_token
        self.time_stop = time_stop #UTC Time
        self.code_metarspeci = 'initial code'
        self.code_taf = 'initial code'
        self.hr = 'time'
        
    def run_MetarSpeci(self):
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(self.chrome_driver,options=options)
            driver.get(self.metarspeci_target);
            sleep(10)
            list_of_elements = driver.find_elements_by_xpath('//p[@class="js-metar"]')
            stations_metarspeci = [station.text for station in list_of_elements];
            find_vtse_metarspeci = [i for i in stations_metarspeci if "VTSE" in i]
            read_metarspeci = find_vtse_metarspeci[0]
            driver.quit()
        
            if read_metarspeci == self.code_metarspeci:
                pass
            else:
                self.code_metarspeci = read_metarspeci
                url = 'https://notify-api.line.me/api/notify'
                token = self.line_token
                headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
                msg = self.code_metarspeci
                r = requests.post(url, headers=headers , data = {'message':msg})        
                print(self.code_metarspeci)

            dt = datetime.datetime.utcnow()
            self.hr = dt.strftime('%H')
            
        except:
            print("METAR or SPECI error")
        
    def run_Taf(self):
        
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            driver = webdriver.Chrome(self.chrome_driver,options=options)
            driver.get(self.taf_target);
            sleep(10)
            list_of_elements = driver.find_elements_by_xpath('//p[@class="js-taf"]')
            stations_taf = [station.text for station in list_of_elements];
            
            find_vtse_taf = [i for i in stations_taf if "VTSE" in i]
            read_taf = find_vtse_taf[0]
            driver.quit()
        
            if read_taf == self.code_taf:
                pass
            else:
                self.code_taf = read_taf
                url = 'https://notify-api.line.me/api/notify'
                token = self.line_token
                headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
                msg = self.code_taf
                r = requests.post(url, headers=headers , data = {'message':msg})        
                print(self.code_taf)
                
        except:
            print("TAF error")
        
class LoopNsweb(MetarSpeciTaf):
    
    def __init__(self, chrome_driver, line_token, time_stop):
        super().__init__(chrome_driver, line_token, time_stop)
        
    def run_loop(self):
        schedule.every().minute.at(":05").do(self.run_MetarSpeci)
        schedule.every().hour.at(":10").do(self.run_Taf)
        while self.hr != self.time_stop:
            schedule.run_pending()
            sleep(1)
            if self.hr == self.time_stop:
                break
        print('Program stopped')