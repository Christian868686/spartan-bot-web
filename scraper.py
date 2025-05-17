from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os

def coletar_dados():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.betano.com.br/jogo/aviator/ ")
        time.sleep(10)

        elementos = driver.find_elements(By.CSS_SELECTOR, ".results-history__item")
        dados = [float(e.text.replace("x", "")) for e in elementos if "x" in e.text]

        df = pd.DataFrame({"multiplicador": dados})
        df.to_csv("data/historico.csv", index=False)

        print("✅ Dados coletados:", dados)
        return True, dados
    except Exception as e:
        print(f"❌ Erro ao coletar dados: {str(e)}")
        return False, []
    finally:
        try:
            driver.quit()
        except:
            pass

# Coleta automática a cada 10 segundos
while True:
    coletar_dados()
    time.sleep(10)