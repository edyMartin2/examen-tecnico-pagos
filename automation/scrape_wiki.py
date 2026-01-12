from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

import requests
import json

def scrape_wikipedia():
    print("Iniciando navegador...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("Navegando a Wikipedia...")
        driver.get("https://es.wikipedia.org/")

        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        
        print("Buscando 'IA'...")
        search_box.send_keys("IA")
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "mw-content-text"))
        )

        content_element = driver.find_element(By.CSS_SELECTOR, "#mw-content-text .mw-parser-output")
        full_text = content_element.text.strip()
        
        if full_text:
            result_text = full_text[:1000]
            print(result_text)
            
            # Send to API
            print("\nEnviando texto a resumir...")
            url = "http://localhost:8000/api/v1/assistant/summarize"
            payload = json.dumps({
                "text": result_text
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': ''
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
            
            if response.status_code == 200:
                print("\n--- Resumen Recibido ---\n")
                print(response.json())
                print("\n------------------------\n")
            else:
                print(f"Error al enviar a la API: {response.status_code} - {response.text}")
                
        else:
            print("No hay articulos.")

        
        time.sleep(2)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        print("Cerrando navegador...")
        driver.quit()

if __name__ == "__main__":
    scrape_wikipedia()
