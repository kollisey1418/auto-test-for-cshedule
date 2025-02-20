import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    datefmt="%Y-%m-%d %H:%M:%S"  # Формат времени
)

logger = logging.getLogger()

CHROME_DRIVER_PATH = "D:/xampp/htdocs/auto-test/chromedriver-win64/chromedriver.exe"

servis=Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=servis)

wait = WebDriverWait(driver, 10)

driver.get("http://localhost/index.html")
logging.info("\U0001F50E Ищем кнопку More Detailed для Свети Стефан")
button = wait.until(EC.element_to_be_clickable((By.ID, "svst")))
logging.info("\u2705 Кнопку нашли, нажимаем")
button.click()
logging.info("\u27a1\ufe0f Перешли на страницу расписания Свети Стефан")

logging.info("\U0001F50E Ищем кнопку Home")
button = wait.until(EC.element_to_be_clickable((By.ID, "homepc")))
logging.info("\u2705 Кнопку нашли, нажимаем")
button.click()


wait.until(EC.presence_of_element_located((By.ID, "svst")))
logging.info("\u27a1\ufe0f Перешли на страницу index.html")

logging.info("\U0001F50E Ищем кнопку More Detailed для Петровац")
button = wait.until(EC.element_to_be_clickable((By.ID, "pet")))
button.click()
logging.info("\u27a1\ufe0f Перешли на страницу расписания Петровац")


driver.quit()
logging.info("\u2705 Браузер закрыт, тест завершён.")