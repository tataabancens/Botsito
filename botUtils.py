from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fillTextInputs(inputs, row):
    for i in range(len(inputs)):
        inputs[i].clear()
        if isinstance(row[i], datetime):
            inputs[i].send_keys(row[i].strftime("%m/%d/%Y"))
            continue
        inputs[i].send_keys(row[i])

# Auto select first option in the radioGroup
def fillRadioGroups(driver):

    radioGroups = driver.find_elements(By.CLASS_NAME, "SG0AAe")
    for radioGroup in radioGroups:
        radioButtons = radioGroup.find_elements(By.CLASS_NAME, "nWQGrd.zwllIb")
        radioButtons[0].click()

def fillDropdown(driver):

    dropdowns = driver.find_elements(By.CLASS_NAME, "jgvuAb.ybOdnf.cGN2le.t9kgXb.llrsB")
    for dropdown in dropdowns:
        dropdown.click()

        # Waits until dropdown shows in screen
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "OA0qNb.ncFHed.QXL7Te")))

        # Selects first option
        dropdownParent = dropdown.find_elements(By.CLASS_NAME, "OA0qNb.ncFHed.QXL7Te")
        dropdownChilds = dropdownParent[0].find_elements(By.CLASS_NAME, "MocG8c")
        dropdownChilds[1].click()

def fillCheckbox(driver):
    checkboxGroups = driver.find_elements(By.CLASS_NAME, "Y6Myld")
    for checkboxGroup in checkboxGroups:
        checkboxes = checkboxGroup.find_elements(By.CLASS_NAME, "eBFwI")
        for checkbox in checkboxes:
            checkbox.click()

def fillForm(driver, row):

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "M7eMe")))
    inputs = driver.find_elements(By.CLASS_NAME, "whsOnd.zHQkBf")
    
    # Llena los inputs de texto con la data del excel
    fillTextInputs(inputs, row)

    # Te dejo comentadas estas tres lineas, para descomentar sacar los numerales
    # Si hay opciones multiples, dropdown o checkbox en el form descomentalas y saca la columna correspondiente del excel si la hubiera
    
    # Llena checkbox
    # fillCheckbox(driver)

    # Llena radio buttons
    # fillRadioGroups(driver)

    # Llena dropdown
    # fillDropdown(driver)
    
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit.click()

    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "vHW8K")))
    
    another_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response.click()