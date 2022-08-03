from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def fillForm(driver, data):
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "M7eMe")))
    inputs = driver.find_elements(By.CLASS_NAME, "whsOnd.zHQkBf")
    
    for i in range(len(inputs)):
        inputs[i].clear()
        inputs[i].send_keys(data[i])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit.click()

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "vHW8K")))

    another_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response.click()