from selenium import webdriver
from time import sleep
import schedule
import datetime
import requests

class MetarSpeciTaf:
    def __init__(self, line_token='', time_stop=''):
        self.metarspeci_target = "https://nsweb.tmd.go.th/#showMetars"
        self.taf_target = "https://nsweb.tmd.go.th/#showTAFs"
        self.line_token = line_token
        self.time_stop = time_stop # UTC Time
        self.code_metarspeci = 'initial_code'
        self.code_taf = 'initial_code'
        self.hr = 'time'
        
    def run_MetarSpeci(self):
        
        options = webdriver.ChromeOptions()
        options.headless = True
        driver_metarspeci = webdriver.Chrome(options=options)
        driver_metarspeci.get(self.metarspeci_target);
        sleep(10)
        
        while self.hr != self.time_stop:
            
            driver_metarspeci.refresh()
            sleep(10)
            
            try:
                list_of_elements = driver_metarspeci.find_elements_by_xpath('//p[@class="js-metar"]')
                stations = [station.text for station in list_of_elements];
                find_vtse = [i for i in stations if "VTSE" in i]
                read = find_vtse[0]
            
                if read == self.code_metarspeci:
                    pass
                else:
                    self.code_metarspeci = read
                    url = 'https://notify-api.line.me/api/notify'
                    token = self.line_token
                    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
                    msg = self.code_metarspeci
                    r = requests.post(url, headers=headers , data = {'message':msg})        
                    print(self.code_metarspeci)

                dt = datetime.datetime.utcnow()
                self.hr = dt.strftime('%H')
                
                if self.hr == self.time_stop:
                    print('Program stopped')
                    break
                else:
                    sleep(40)
                    
            except Exception as e:
                
                print("METAR or SPECI error: " ,e)
                dt = datetime.datetime.utcnow()
                self.hr = dt.strftime('%H')
                
                if self.hr == self.time_stop:
                    print('Program stopped')
                    break
                else:
                    sleep(40)
                    
        driver_metarspeci.quit()
            
    def run_Taf(self):
                
        options = webdriver.ChromeOptions()
        options.headless = True
        driver_taf = webdriver.Chrome(options=options)
        driver_taf.get(self.taf_target);
        sleep(10)
        
        while True:
            
            driver_taf.refresh()
            sleep(10)
            
            try:
                list_of_elements = driver_taf.find_elements_by_xpath('//p[@class="js-taf"]')
                stations = [station.text for station in list_of_elements];
                find_vtse = [i for i in stations if "VTSE" in i]
                read = find_vtse[0]
            
                if read == self.code_taf:
                    pass
                else:
                    self.code_taf = read
                    url = 'https://notify-api.line.me/api/notify'
                    token = self.line_token
                    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
                    msg = self.code_taf
                    r = requests.post(url, headers=headers , data = {'message':msg})        
                    print(self.code_taf)

                dt = datetime.datetime.utcnow()
                self.hr = dt.strftime('%H')
                
            except Exception as e:
                dt = datetime.datetime.utcnow()
                self.hr = dt.strftime('%H')
                print("TAF error: ", e)
                
            else:
                print('Achieved')
                break
            
        driver_taf.quit()
            
        
    def loop_Taf(self):
        
        schedule.every().hour.at(":05").do(self.run_Taf)
        
        while self.hr != self.time_stop:
            schedule.run_pending()
            sleep(1)
            if self.hr == self.time_stop:
                break
        print('Program stopped')