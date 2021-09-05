from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
from os import makedirs



from config import USERNAME, PASSWORD, BROWSEROPTIONS, logging



class BrickBot():
    def __init__(self):
        self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=BROWSEROPTIONS)
        self.driver.implicitly_wait(10) # seconds
        

    @staticmethod
    def save_page(driver, path):
        source = driver.page_source
        with open(path, 'w') as file:
            file.writelines(source)

    def login(self):
        logging.info('logining')
        self.driver.get('https://www.bricklink.com/')

        close_but = self.driver.find_element_by_xpath('//*[@id="js-btn-save"]/button[1]')   
        #close_but = self.driver.find_element_by_xpath('//*[@id="js-btn-save"]/button[1]')
        close_but.click()

        log_but = self.driver.find_element_by_xpath('//*[@id="nav-login-button"]')
        log_but.click() 

        log_inp = self.driver.find_element_by_xpath('//*[@id="usernameOrEmail"]')  
        log_inp.send_keys(USERNAME)

        pas_inp = self.driver.find_element_by_xpath('//*[@id="password"]')  
        pas_inp.send_keys(PASSWORD)

        log_but = self.driver.find_element_by_xpath('//*[@id="signupContainer"]/div/div[2]/div/div[2]/div/button')
        log_but.click()

    def load_wishlist(self, wishlist_name):
        self.driver.find_element_by_xpath('//*[@id="nav-me"]/button').click()
        self.driver.find_element_by_xpath('//*[@id="mybl"]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/img').click()
    
        # go to whishlist page
        self.driver.find_element_by_xpath(f'//*[text()="{wishlist_name}"]').click()
    
    def load_shop(self,shop_id,wishlists_name):
        base_path = f'pages//{"_".join([f[:4] for f in wishlists_name])}//{shop_id}'
        makedirs(base_path, exist_ok=True)
        
        

        sleep(0.5)
        logging.info(f'Going to {shop_id=}')
        self.driver.get(f'https://store.bricklink.com/{shop_id}#/shop')  # go to store page

        #self.driver.find_element_by_xpath('//*[@id="store-nav-menu"]/ul[1]/li[1]/a').click() # click shop tab
        self.driver.find_element_by_xpath('//*[@id="storeApp"]/div/div[3]/div[2]/div[1]/ul/li[4]/a').click()  # click wishlisttab

        self.driver.find_element_by_xpath('//*[@id="advSearch"]/div/div[2]/section/div[1]/label/small').click()  # deselect all
        sleep(1)

        if type(wishlists_name) == type([]):  # select wishlists or only one
            for wishlist_name in wishlists_name:  # if is ar array then iterate over it
                logging.info(f'Selecting {wishlist_name=}')
                self.driver.find_element_by_xpath(f'//*[text()="{wishlist_name}"]').click()
                sleep(0.25)
        else:  #otherwise handle it just like a string
            logging.info(f'Selecting {wishlists_name=}')
            self.driver.find_element_by_xpath(f'//*[text()="{wishlists_name}"]').click()
        logging.info('Done selecting')

        num_of_parts_per_page = self.driver.find_element_by_xpath('//*[@id="storeApp"]//select[@name="pgSize"]')       
        num_of_parts_per_page = Select(num_of_parts_per_page) # select drop down menu where you can choose the number of parts per page
        num_of_parts_per_page.select_by_value('100') # select 100 parts per page


        num_pages = self.driver.find_element_by_xpath('//*[@id="storeApp"]//ul[@class="pagination"]')
        num_pages = num_pages.text.split('\n')[-2] 
        for page_number in range(1,int(num_pages)+1):  # iterate over pages
            logging.info(f'Saving page: {page_number}')
            saving_path = f'{base_path}//page{str(page_number)}.html'

            BrickBot.save_page(self.driver, saving_path)  # save page source
            self.driver.find_element_by_xpath('//*[@id="storeApp"]//a[@aria-label="Next"]').click()
            # click 'next page' button
            self.driver.find_element_by_xpath('//*[@id="storeApp"]//div[@class="table-header-image"]')  # wait until page is loaded
                
    
    def quit(self):
        self.driver.close()

if __name__ == '__main__':
    bot = BrickBot()
    bot.login()
    wanted_lists = ['mecjh','frame+armored','mixels parts','parta essentials']
    bot.load_shop('gritts',wanted_lists)
    bot.load_shop('michek',wanted_lists)
    bot.load_shop('rafgier',wanted_lists)
    
    
    bot.quit()