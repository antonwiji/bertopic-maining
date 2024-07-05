import re
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# Konfigurasi path untuk chromedriver
executable_path = r"C:\Anton\Learn\tools\chromedriver.exe"
service = Service(executable_path)

# Opsi untuk Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument('--ignore-certificate-errors')

# Inisialisasi driver
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://search.kompas.com/search/?q=prabowo&submit=Submit#gsc.tab=0&gsc.q=prabowo&gsc.page=0")

def clean_text(data):
    # Remove non-ASCII characters
    cleaned_data = re.sub(r'[^\x00-\x7F]+', '', data)
    return cleaned_data

# Menunggu dan mencari elemen yang akan diklik
try:
    data = []
    elements_contents = driver.find_elements(By.CSS_SELECTOR, 'div.gs-title a')
    for index in range(15):
            try:
                # Mengambil ulang elemen setiap iterasi untuk menghindari StaleElementReferenceException
                elements_contents = driver.find_elements(By.CSS_SELECTOR, 'div.gs-title a')
                data_content = elements_contents[index]

                # Menunggu elemen menjadi interaktif
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.gs-title a')))

                # Klik elemen
                driver.execute_script("arguments[0].click();", data_content)
                time.sleep(3)  # Menunggu beberapa detik agar halaman tujuan dimuat

                # Mengambil teks dari elemen berita
                elements_berita = driver.find_elements(By.CSS_SELECTOR, 'div.read__content p')
                deskripsi = []
                for berita in elements_berita:
                    clean_data = clean_text(berita.text)
                    deskripsi.append(clean_data)
                    print(berita.text)
                deskripsi = [' '.join(deskripsi)]
                data.append(deskripsi)
                # Kembali ke halaman sebelumnya
                driver.execute_script("window.history.go(-1)")
                time.sleep(3)  # Menunggu beberapa detik agar halaman sebelumnya dimuat

            except StaleElementReferenceException as e:
                print(f"Stale element reference error: {e}")
                driver.back()
                print(f"Error: {e}")
                df = pd.DataFrame(data, columns=["berita"])
                df.to_csv('berita.csv', index=False)
                time.sleep(3)  # Menunggu beberapa detik agar halaman sebelumnya dimuat
                continue
            except ElementNotInteractableException as e:
                print(f"Element not interactable error: {e}")
                driver.back()
                df = pd.DataFrame(data, columns=["berita"])
                df.to_csv('berita.csv', index=False)
                time.sleep(3)  # Menunggu beberapa detik agar halaman sebelumnya dimuat
                continue
    # Membuat DataFrame dari list data setelah loop selesai
    df = pd.DataFrame(data, columns=["berita"])
    df.to_csv('berita9.csv', index=False)

except (NoSuchElementException, ElementNotInteractableException) as e:
    print(f"Error: {e}")
    df = pd.DataFrame(data, columns=["berita"])
    df.to_csv('berita9.csv', index=False)

finally:
    driver.quit()
