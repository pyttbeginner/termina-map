from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
import re
import time

os.makedirs("maps", exist_ok=True)

HEADERS = {
    "User-Agent": "Maria/FearHungerMaps (maria@example.com)"
}

driver = webdriver.Chrome()

try:
    driver.get("https://fearandhunger.wiki.gg/wiki/Category:Maps_F%26H2")
    time.sleep(5)
    
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "a.image img")
    print(f"Найдено миниатюр: {len(thumbnails)}")
    
    for i, img in enumerate(thumbnails):
        thumb_src = img.get_attribute("src")
        
        match = re.search(r'/images/thumb/.*?/\d+px-(.*?)(?:\?|$)', thumb_src)
        if match:
            filename = match.group(1)
            full_url = "https://fearandhunger.wiki.gg/images/" + filename
            
            try:
                img_data = requests.get(full_url, headers=HEADERS).content
                
                # Проверяем что это не ошибка
                if len(img_data) < 1000:
                    print(f"[{i+1}/{len(thumbnails)}] Пропуск (ошибка): {filename}")
                    continue
                
                with open(f"maps/{filename}", "wb") as f:
                    f.write(img_data)
                print(f"[{i+1}/{len(thumbnails)}] {filename}")
                
                # Задержка чтобы не блокировали
                time.sleep(0.5)
                
            except Exception as e:
                print(f"[{i+1}/{len(thumbnails)}] Ошибка: {filename} - {e}")
    
    print("Готово!")
    
finally:
    driver.quit()
