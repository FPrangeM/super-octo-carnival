import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options




class WebAutomator:
    def __init__(self, t_wait=120, download_pref=1, download_path='', driver='firefox', options_dict={}, proxy=False):
        # Configuração da pasta destino download
        if download_pref == 1:
            download_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
        elif download_pref == 2:
            download_path = r'P:\COMUM\FALCAO\30. EBB\30.Jasper_Files'

        self.download_path = download_path
        self.t_wait = t_wait
        if proxy:
            os.environ['https_proxy'] = 'http://10.105.160.5:8080'

        # Configuração em caso de Firefox
        if driver == 'firefox':
            options = webdriver.FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", download_path)
            self.driver = webdriver.Firefox(options=options)
        # Configuração em caso de Chrome
        elif driver == 'chrome':
            options = Options()
            for key, value in options_dict.items():
                options.add_argument(f'--{key}={value}')

            options.add_experimental_option("prefs", {
                "download.default_directory": download_path,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            self.driver = webdriver.Chrome(options=options)

    def wait_element(self, xpath):
        element = WebDriverWait(self.driver, self.t_wait).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return element

    def sendkey_wait(self, xpath, keys):
        t1=time.time()
        while time.time()-t1 <= self.t_wait:
            try:
                WebDriverWait(self.driver, self.t_wait).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(keys)
                break
            except (ElementNotInteractableException):
                time.sleep(0.5)
                pass

    def click_wait(self,xpath):
        t1=time.time()
        while time.time()-t1 <= self.t_wait:
            element = WebDriverWait(self.driver, self.t_wait).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            try:
                element.click()
                break
            except (ElementClickInterceptedException,ElementNotInteractableException):
                time.sleep(0.5)
                pass

    def clear_wait(self, xpath):
        WebDriverWait(self.driver, self.t_wait).until(EC.element_to_be_clickable((By.XPATH, xpath))).clear()

    def wait_invisibility(self,xpath):
        WebDriverWait(self.driver,self.t_wait).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        pass

    def recursive_iframe_finder(self, element_xpath, lstring=''):
        try:
            element = self.driver.find_element(By.XPATH, element_xpath)
            return element
        except NoSuchElementException:
            iframes = self.driver.find_elements(By.TAG_NAME, 'iframe')
            for k, iframe in enumerate(iframes):
                self.driver.switch_to.frame(iframe)
                result = self.recursive_iframe_finder(element_xpath, lstring + str(k))
                if result:
                    # print(lstring)
                    # print(iframe)
                    return result
                self.driver.switch_to.parent_frame()

    def wait_downloads(self, n_downloads):
        self.t_wait = 2*self.t_wait
        cwh = self.driver.current_window_handle
        l1=self.driver.window_handles
        l2=l1
        self.driver.execute_script("window.open('');") 
        while len(l2) == len(l1):
            time.sleep(0.3)
            l2 = self.driver.window_handles
        dwh=set(l1).symmetric_difference(set(l2)).pop()
        self.driver.switch_to.window(dwh) 
        self.driver.get("about:downloads")
        time.sleep(0.3)
        self.wait_element('//*[@state="1"]')
        t1=time.time()

        while time.time()-t1 <= self.t_wait:
            d = len(self.driver.find_elements(By.XPATH,'//*[@state="1"]'))
            if d >= n_downloads:
                d_stat='Concluido'
                break
            time.sleep(0.3)
        if d_stat:
            print('Downloads Finalizados') 
        else:
            print('Download incompleto, Tempo Expirado') 
        self.driver.close()
        self.driver.switch_to.window(cwh)
        self.t_wait = self.t_wait/2

    def wait_for_page_to_load(self):
        # print('esperando pagina carregar...')
        t1=time.time()
        WebDriverWait(self.driver, self.t_wait).until(lambda driver: driver.execute_script('return document.readyState') == 'loading')
        WebDriverWait(self.driver, self.t_wait).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        t2=time.time()
