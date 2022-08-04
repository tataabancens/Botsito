from botUtils import fillForm
from selenium import webdriver

import pandas as pd
excel_file = 'Raffle EXCEL.xlsx'

# df = Data frame
df = pd.read_excel(excel_file)

# Opening form in chrome
driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")
url = "https://docs.google.com/forms/d/e/1FAIpQLScQnvHzi7jf3pWUyAzv34z12EnNnPdBDYAhwlHPMvRr4lpL7w/viewform"
driver.get(url)

for index, row in df.iterrows():
    # filling and submiting form
    fillForm(driver, row)
