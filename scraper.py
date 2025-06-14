from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_exchange_data():
    options = Options()
    options.add_argument("--headless")  # Opens the browser incognito
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.doviz.com/")

    exchange_data = {}

    try:
        wait = WebDriverWait(driver, 15)  # Waits up to 15 seconds

        usd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-socket-key="USD"]'))).text.strip()
        eur = driver.find_element(By.CSS_SELECTOR, 'span[data-socket-key="EUR"]').text.strip()
        gram_gold = driver.find_element(By.CSS_SELECTOR, 'span[data-socket-key="gram-altin"]').text.strip()

        try:
            quarter_gold = driver.find_element(By.CSS_SELECTOR, 'span[data-socket-key="ceyrek-altin"]').text.strip()
        except:
            quarter_gold = "N/A"

        exchange_data["USD"] = usd
        exchange_data["EUR"] = eur
        exchange_data["Gram Gold"] = gram_gold
        exchange_data["Quarter Gold"] = quarter_gold

    except Exception as e:
        print("Error while extracting data:", e)
        exchange_data = None

    driver.quit()
    return exchange_data
