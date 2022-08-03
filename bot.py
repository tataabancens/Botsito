from botUtils import fillForm
from selenium import webdriver

# Opening form in chrome
driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe")
url = "https://docs.google.com/forms/d/e/1FAIpQLScQnvHzi7jf3pWUyAzv34z12EnNnPdBDYAhwlHPMvRr4lpL7w/viewform"
driver.get(url)

data = ["Abancens", "Avellaneda 657", "42231327"]
# filling and submiting form
fillForm(driver, data)