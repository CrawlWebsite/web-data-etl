from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from config.logger import LoggerCustom 

from real_estate_etl.jobs.converters.composite_item_converter import CompositeItemConverter
from real_estate_etl.jobs.importers.base_importer import BaseImporter


class WebDriverImporter(BaseImporter):

    def __init__(self, converters=()):
        self.converter = CompositeItemConverter(converters)

        self.options = self.get_options()

        self.logger = LoggerCustom(WebDriverImporter.__name__)

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()

        # Set options to make the ChromeDriver less detectable
        options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')  # Disable loading of images
        options.add_argument('--enable-blink-features=DisableJavaScript')  # Disable JavaScript execution

        return options
    
    def create_driver(self, url: str, cmd: str, postData=None):
        try:
            url = f"{API_HOST}/api/web-page?cmd={cmd}&path={url}"
            if postData:
                url = url + f'&postData={postData}'

            driver = webdriver.Chrome(options=self.options)
            driver.get(url)
            driver.maximize_window()

            self.logger.info(f"Get page {url} successful")
        except Exception as ex:
            print(ex)
            sleep(10)
            driver.get(url)

        return driver
    
    def getElementByClass(self, className):
        return self.driver.find_elements(By.CLASS_NAME, className)
    
    def getElementByCssSelector(self, css_selector):
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)

    def open(self):
        pass

    def import_items(self, queries):
        list_data = []
        for query in queries:
            data = self.import_item(query)
            list_data.append(data)

        return list_data

    def import_item(self, query):
        url = query.where['url']

        driver = self.create_driver(url=url, cmd='get')
        page_source = driver.page_source

        return page_source

    def convert_items(self, items):
        pass

    def close(self):
        pass

    