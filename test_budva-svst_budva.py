import json
import os

from selenium import webdriver  # Для управления браузером
from selenium.webdriver.common.by import By  # Для поиска элементов
from selenium.webdriver.support.ui import WebDriverWait  # Для ожиданий
from selenium.webdriver.support import expected_conditions as EC  # Для задания условий ожидания
from selenium.webdriver.chrome.service import Service  # Для управления драйвером
from datetime import datetime

import pytest
import logging
import random

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    datefmt="%Y-%m-%d %H:%M:%S"  # Формат времени
)

logger = logging.getLogger()





CHROME_DRIVER_PATH = "D:/xampp/htdocs/auto-test/chromedriver-win64/chromedriver.exe"  # Укажите реальный путь
active_schedule_path = "D:/xampp/htdocs/html_schedual/active_schedule.json"
json_folder = "D:/xampp/htdocs/html_schedual"


@pytest.fixture
def driver():
    # Инициализация WebDriver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    yield driver  # Возвращаем WebDriver для использования в тесте
    driver.quit()  # Закрываем WebDriver после завершения теста


def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

def validate_schedule_budva_to_sv_st(driver, interval, active_schedule_path, json_folder):

    table = driver.find_element(By.ID, "result")
    table_html = table.get_attribute("innerHTML")

    with open(active_schedule_path, "r") as active_file:
        active_data = json.load(active_file)
        active_state = active_data["active"]

        json_file = f"budva_sveti_stefan_{active_state}.json"
        json_path = os.path.join(json_folder, json_file)

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Файл {json_path} не найден")

    with open(json_path, "r") as schedule_file:
        schedule_data = json.load(schedule_file)

        times_in_json = [parse_time(entry["time"]) for entry in schedule_data]
        logging.info(f"Время из {times_in_json}")

        start_time, end_time = map(parse_time, interval.split("-"))
        time_in_json = any(start_time <= time <= end_time for time in times_in_json)

        table_times = [td.text for td in table.find_elements(By.TAG_NAME, "td")]
        time_in_table = any(start_time <= time <= end_time for time in table_times)

    if not time_in_table and time_in_json:
        raise  AssertionError(f"\u274c Ошибка: Расписание для интервала {interval} отсутствует на странице, но есть в JSON!")
    elif not time_in_table and not time_in_json:
        logging.info(f" \u274c Расписание для интервала {interval} отсутствует как на странице, так и в JSON. Это корректно.")
    else:
        logging.info(f"\u274c Расписание для интервала {interval} корректно отображено на странице.")


        
def test_budva_to_sv_st(driver):
    driver.get("http://localhost/budva-sveti-stefan-budva.html") #Открытие страницы



    stops = ["Budva", "Crvena Zgrada", "Stadion", "Aqua park", "Moc (SkyLine)", "Bella Vista", "Rafailovichi", "Kamenovo", "Maestral", "Przhno", "Sveti Stefan"]
    intervals = ["06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "22:00-00:00"]

    for departure in stops:
            departure_index = stops.index(departure)
            posible_arrivals = stops[departure_index + 1:]

            for arrival in posible_arrivals:
                for interval in intervals:
                    try:

                # Логирование только после определения переменных
                        selected_departure = None
                        selected_arrival = None
                        selected_interval = None


                        logging.debug("\U0001F50E --------Поиск кнопки detailedScheduleButton--------")
                        detailed_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "detailedScheduleButton"))  # Предположим, что у кнопки есть ID
                            )
                        logging.info("Пробуем нажать на Detailed Schedule")
                        detailed_button.click()
                        logging.info("\u2705 Кнопка нажата")


                        logging.info("Ожидаем открытия попуп")
                        popup = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, "schedulePopup"))  # Предположим, что у попапа есть ID
                        )
                        logging.info("\u2705 Окно открылось")

                        logging.info("\U0001F50E Ищем кнопку ShowAll")
                        show_all_button = popup.find_element(By.ID, "showAllButton")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Show All")
                        show_all_button.click()
                        logging.info("\u2705 Кнопка Show All нажата")

                        logging.info("waiting the table")
                        table = WebDriverWait(popup, 10).until(
                            EC.presence_of_element_located((By.ID, "result"))  # ID таблицы внутри попапа
                            )
                        logging.info("\u2705 table is loaded")
                        assert table.is_displayed(), "Ошибка: таблица не отображается!"

#Select Departure--------------------------
                        logging.info("\U0001F50E Ищем кнопку Select Departure")
                        departure_Button = popup.find_element(By.ID, "departureButton")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Select Departure")
                        departure_Button.click()
                        logging.info("\u2705 Кнопка Select Departure нажата")


                        logging.info("Ожидаем выпадание списка")
                        departure_dropdown = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, "departureDropdown"))  # Предположим, что у попапа есть ID
                            )
                        logging.info("\u2705 Список выпал")


                    # Проверяем, что список видим
                        display_style = departure_dropdown.value_of_css_property("display")
                        logging.info(f"Текущий стиль display: {display_style}")
                        assert display_style == "block", "Ошибка: выпадающий список не отображается!"

                        logging.info("\U0001F50E Выбираем элемент из списка")
                        options = departure_dropdown.find_elements(By.TAG_NAME, "a")
                        assert len(options) > 0, "Ошибка: список пуст!"

                    # Выбрать случайный элемент из списка
                        logging.info("\U0001F50E Выбирает рандомную ссылку")
                        random_departure = random.choice(options)
                        selected_departure = random_departure.text
                        logging.info(f"\u2705 Рандомная ссылка выбрана: {random_departure.text}")

                        random_departure.click()
                    #test push./

#Select Arrival--------------------------

                        logging.info("\U0001F50E Ищем кнопку Select Arrival")
                        arrival_Button = popup.find_element(By.ID, "arrivalButton")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Select Arrival")
                        arrival_Button.click()
                        logging.info("\u2705 Кнопка Select Arrival нажата")


                    # Ожидаем обновления списка Arrival
                        logging.info("Ожидаем обновление выпадающего списка Arrival")
                        WebDriverWait(driver, 10).until(
                            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#arrivalDropdown li a")) > 0
                            )

                        arrival_dropdown = popup.find_element(By.ID, "arrivalDropdown")
                        arrival_options = arrival_dropdown.find_elements(By.TAG_NAME, "a")

                    # Проверяем, что список Arrival обновлен
                        assert len(arrival_options) > 0, f"Ошибка: список Arrival не обновился для станции {selected_departure}!"
                        logging.info(f"\u2705 Список Arrival обновлен: {[option.text for option in arrival_options]}")

                    # Выбираем случайную станцию Arrival
                        random_arrival = random.choice(arrival_options)
                        selected_arrival = random_arrival.text
                        logging.info(f"\u2705 Случайная станция прибытия выбрана: {selected_arrival}")
                        random_arrival.click()
                        #test push./


#Select Interval-------------------------------
                        logging.info("\U0001F50E Ищем кнопку Select Time Interval")
                        intervalButton = popup.find_element(By.ID, "intervalButton")
                        logging.info("Пробуем нажать кнопку")
                        intervalButton.click()
                        logging.info("\u2705 Кнопка нажата")

                        logging.info("Ожидаем выпадание списка")
                        intervalDropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "intervalDropdown")) )
                        logging.info("\u2705 Список выпал")


                        display_style = intervalDropdown.value_of_css_property("display")
                        logging.info(f"Текущий стиль display: {display_style}")
                        assert display_style == "block", "Ошибка: выпадающий список не отображается!"

                        logging.info("\U0001F50E Выбираем элемент из списка")
                        options = intervalDropdown.find_elements(By.TAG_NAME, "a")
                        assert len(options) > 0, "Ошибка: список пуст!"

                        logging.info("\U0001F50E Выбираем рандомную ссылку")
                        random_interval = random.choice(options)
                        selected_interval = random_interval.text
                        logging.info(f"\u2705 Рандомная ссылка выбрана: {selected_interval}")

                        random_interval.click()

                        logging.info("\U0001F50E Ищем кнопку Finde Schedule")
                        searchButton = popup.find_element(By.ID, "searchButton")
                        logging.info("Нажимаем жимаем на Finde Schedule")
                        searchButton.click()
                        logging.info("\u2705 Search Button нажата")

                        logging.info("Ждем таблицу")
                        table = WebDriverWait(popup, 10).until(EC.visibility_of_element_located((By.ID, "result")) )
                        logging.info("\u2705 Таблица загружена")
                        assert table.is_displayed(), "Ошибка: Таблица не отображается!"

                        table_html = table.get_attribute("innerHTML")
                        logging.info(f"Содержание таблицы: {table_html}")

                        assert selected_departure in table_html, f"Ошибка: станция отправления '{selected_departure}' отсутствует в таблице!"
                        assert selected_arrival in table_html, f"Ошибка: станция назначения '{selected_arrival}' отсутствует в таблице!"

                        logging.info("Извлекаем время из таблицы")
                        table_times = [td.text for td in table.find_elements(By.TAG_NAME, "td")]
                        logging.info("\u2705 Время извлечено")

                        logging.info("Разбираем временный интервал")
                        start_time, end_time = selected_interval.split("-")

                        logging.info("Проверяем, что хотя бы одно время из интервала есть в таблице")
                        if start_time > end_time:
                            time_in_range = any(time >= start_time or time <= end_time for time in table_times if time)
                        else:
                            time_in_range = any(start_time <= time <= end_time for time in table_times if time)
                        assert time_in_range, f"Ошибка: Временной интервал {selected_interval} не найден в таблице!"
                        logging.info("\u2705 Интервал времени найден в таблице.")

                        try:
                            logging.info("\U0001F50E Ищем кнопку закрытия попап окна")
                            closePopup = popup.find_element(By .ID, "closePopup")
                            logging.info("Try to click")
                            closePopup.click()
                            logging.warning("\u2705 --------Попуп окно закрылось--------")
                        except Exception:
                            logging.warning("Не удалось закрыть Popup, возможно он уже закрыт")

                        logging.info(
                            f"Тестировались значения: Departure='{selected_departure}', Arrival='{selected_arrival}', Interval='{selected_interval}'")

                        pass
                    except Exception as e:
                        # Логируем ошибку для каждой комбинации
                        logging.error(f"Ошибка для комбинации Departure='{departure}', Arrival='{arrival}', Interval='{interval}': {e}")

                        try:
                            closePopup = popup.find_element(By. ID, "closePopup")
                            closePopup.click()
                            logging.warning("closePopup закрыт после ошибки")
                        except Exception: ("\u2705 Popup был закрыт штатно")
                        continue  # Продолжаем цикл даже при ошибке






#------------------------------------------------------------------


def validate_schedule_sv_st_to_budva(driver, interval, active_schedule_path, json_folder):

    table = driver.find_element(By.ID, "result2")
    table_html = table.get_attribute("innerHTML")

    with open(active_schedule_path, "r") as active_file:
        active_data = json.load(active_file)
        active_state = active_data["active"]

        json_file = f"sveti_stefan_budva_{active_state}.json"
        json_path = os.path.join(json_folder, json_file)

        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Файл {json_path} не найден")

    with open(json_path, "r") as schedule_file:
        schedule_data = json.load(schedule_file)

        times_in_json = [parse_time(entry["time"]) for entry in schedule_data]
        logging.info(f"Время из {times_in_json}")

        start_time, end_time = map(parse_time, interval.split("-"))
        time_in_json = any(start_time <= time <= end_time for time in times_in_json)

        table_times = [td.text for td in table.find_elements(By.TAG_NAME, "td")]
        time_in_table = any(start_time <= time <= end_time for time in table_times)

    if not time_in_table and time_in_json:
        raise  AssertionError(f"\u274c Ошибка: Расписание для интервала {interval} отсутствует на странице, но есть в JSON!")
    elif not time_in_table and not time_in_json:
        logging.info(f"Расписание для интервала {interval} отсутствует как на странице, так и в JSON. Это корректно.")
    else:
        logging.info(f"Расписание для интервала {interval} корректно отображено на странице.")

def test_sv_st_to_budva(driver):
    driver.get("http://localhost/budva-sveti-stefan-budva.html") #Открытие страницы
    logging.info("начинаем тест")



    stops2 = ["Budva", "Crvena Zgrada", "Stadion", "Aqua park", "Moc (SkyLine)", "Bella Vista", "Rafailovichi", "Kamenovo", "Maestral", "Przhno", "Sveti Stefan"]
    intervals2 = ["06:00-08:00", "08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "22:00-00:00"]
    logging.info("Определяем массив остановок и время")
    for departure2 in stops2:
            departure2_index = stops2.index(departure2)
            posible_arrivals2 = stops2[departure2_index + 1:]
            logging.info("\u2705 Настроили кнопку arrival")

            for arrival2 in posible_arrivals2:
                for interval2 in intervals2:
                    try:
                        logging.info("пробуем искать кнопку schedule Button2")
                # Логирование только после определения переменных
                        selected_departure2 = None
                        selected_arrival2 = None
                        selected_interval2 = None
                        logging.info("\u2705 Определили переменные")

                        logging.info("\U0001F50E --------Поиск кнопки ScheduleButton2--------")
                        detailed_button2 = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "scheduleButton2"))  # Предположим, что у кнопки есть ID
                            )
                        logging.info("Пробуем нажать на Detailed Schedule")
                        detailed_button2.click()
                        logging.info("\u2705 Кнопка нажата")


                        logging.info("Ожидаем открытия попуп")
                        popup = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, "schedulePopup2"))  # Предположим, что у попапа есть ID
                        )
                        logging.info("\u2705 Окно открылось")

                        logging.info("\U0001F50E Ищем кнопку ShowAll")
                        show_all_button2 = popup.find_element(By.ID, "showAllButton2")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Show All")
                        show_all_button2.click()
                        logging.info("\u2705 Кнопка Show All нажата")

                        logging.info("waiting the table")
                        table = WebDriverWait(popup, 10).until(
                            EC.presence_of_element_located((By.ID, "result2"))  # ID таблицы внутри попапа
                            )
                        logging.info("table is loaded")
                        assert table.is_displayed(), "\u274c Ошибка: таблица не отображается!"

#Select Departure--------------------------
                        logging.info("\U0001F50E Ищем кнопку Select Departure")
                        departure_Button2 = popup.find_element(By.ID, "departureButton2")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Select Departure")
                        departure_Button2.click()
                        logging.info("\u2705 Кнопка Select Departure нажата")


                        logging.info("Ожидаем выпадание списка")
                        departure_dropdown2 = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.ID, "departureDropdown2"))  # Предположим, что у попапа есть ID
                            )
                        logging.info("\u2705 Список выпал")


                    # Проверяем, что список видим
                        display_style = departure_dropdown2.value_of_css_property("display")
                        logging.info(f"Текущий стиль display: {display_style}")
                        assert display_style == "block", "\u274c Ошибка: выпадающий список не отображается!"

                        logging.info("\U0001F50E Выбираем элемент из списка")
                        options = departure_dropdown2.find_elements(By.TAG_NAME, "a")
                        assert len(options) > 0, "\u274c Ошибка: список пуст!"

                    # Выбрать случайный элемент из списка
                        logging.info("\U0001F50E Выбирает рандомную ссылку")
                        random_departure2 = random.choice(options)
                        selected_departure2 = random_departure2.text
                        logging.info(f"\u2705 Рандомная ссылка выбрана: {random_departure2.text}")

                        random_departure2.click()
                    #test push./

#Select Arrival--------------------------

                        logging.info("\U0001F50E Ищем кнопку Select Arrival")
                        arrival_Button2 = popup.find_element(By.ID, "arrivalButton2")  # Найти кнопку внутри попапа
                        logging.info("Пробуем нажать на кнопку Select Arrival")
                        arrival_Button2.click()
                        logging.info("\u2705 Кнопка Select Arrival нажата")


                    # Ожидаем обновления списка Arrival
                        logging.info("Ожидаем обновление выпадающего списка Arrival")
                        WebDriverWait(driver, 10).until(
                            lambda d: len(d.find_elements(By.CSS_SELECTOR, "#arrivalDropdown2 li a")) > 0
                            )

                        arrival_dropdown2 = popup.find_element(By.ID, "arrivalDropdown2")
                        arrival_options = arrival_dropdown2.find_elements(By.TAG_NAME, "a")

                    # Проверяем, что список Arrival обновлен
                        assert len(arrival_options) > 0, f"\u274c Ошибка: список Arrival не обновился для станции {selected_departure2}!"
                        logging.info(f"\u2705 Список Arrival обновлен: {[option.text for option in arrival_options]}")

                    # Выбираем случайную станцию Arrival
                        random_arrival2 = random.choice(arrival_options)
                        selected_arrival2 = random_arrival2.text
                        logging.info(f"\u2705 Случайная станция прибытия выбрана: {selected_arrival2}")
                        random_arrival2.click()
                        #test push./


#Select Interval-------------------------------
                        logging.info("\U0001F50E Ищем кнопку Select Time Interval")
                        intervalButton2 = popup.find_element(By.ID, "intervalButton2")
                        logging.info("Пробуем нажать кнопку")
                        intervalButton2.click()
                        logging.info("\u2705 Кнопка нажата")

                        logging.info("Ожидаем выпадание списка")
                        intervalDropdown2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "intervalDropdown2")) )
                        logging.info("\u2705 Список выпал")


                        display_style = intervalDropdown2.value_of_css_property("display")
                        logging.info(f"Текущий стиль display: {display_style}")
                        assert display_style == "block", "\u274c Ошибка: выпадающий список не отображается!"

                        logging.info("\U0001F50E Выбираем элемент из списка")
                        options = intervalDropdown2.find_elements(By.TAG_NAME, "a")
                        assert len(options) > 0, "\u274c Ошибка: список пуст!"

                        logging.info("\U0001F50E Выбираем рандомную ссылку")
                        random_interval2 = random.choice(options)
                        selected_interval2 = random_interval2.text
                        logging.info(f"\u2705 Рандомная ссылка выбрана: {selected_interval2}")

                        random_interval2.click()

                        logging.info("\U0001F50E Ищем кнопку Finde Schedule")
                        searchButton2 = popup.find_element(By.ID, "searchButton2")
                        logging.info("Нажимаем жимаем на Finde Schedule")
                        searchButton2.click()
                        logging.info("\u2705 Search Button нажата")

                        logging.info("\U0001F50E Ждем таблицу")
                        table = WebDriverWait(popup, 10).until(EC.visibility_of_element_located((By.ID, "result2")) )
                        logging.info("\u2705 Таблица загружена")
                        assert table.is_displayed(), "\u274c Ошибка: Таблица не отображается!"

                        table_html = table.get_attribute("innerHTML")
                        logging.info(f"Содержание таблицы: {table_html}")

                        assert selected_departure2 in table_html, f"\u274c Ошибка: станция отправления '{selected_departure2}' отсутствует в таблице!"
                        assert selected_arrival2 in table_html, f"\u274c Ошибка: станция назначения '{selected_arrival2}' отсутствует в таблице!"

                        logging.info("Извлекаем время из таблицы")
                        table_times = [td.text for td in table.find_elements(By.TAG_NAME, "td")]
                        logging.info("\u2705 Время извлечено")

                        logging.info("Разбираем временный интервал")
                        start_time, end_time = selected_interval2.split("-")

                        logging.info("Проверяем, что хотя бы одно время из интервала есть в таблице")
                        if start_time > end_time:
                            time_in_range = any(time >= start_time or time <= end_time for time in table_times if time)
                        else:
                            time_in_range = any(start_time <= time <= end_time for time in table_times if time)
                        assert time_in_range, f"\u274c Ошибка: Временной интервал {selected_interval2} не найден в таблице!"
                        logging.info("\u2705 Интервал времени найден в таблице.")

                        logging.info("\U0001F50E Ищем кнопку закрытия попап окна")
                        closePopup = popup.find_element(By .ID, "closePopup2")
                        logging.info("Try to click")
                        closePopup.click()
                        logging.warning("\u2705 --------Попуп окно закрылось--------")

                        logging.info(
                            f"Тестировались значения: Departure='{selected_departure2}', Arrival='{selected_arrival2}', Interval='{selected_interval2}'")

                        pass
                    except Exception as e:
                        # Логируем ошибку для каждой комбинации
                        logging.error(f"\u274c Ошибка для комбинации Departure='{departure2}', Arrival='{arrival2}', Interval='{interval2}': {e}")


                    try:
                        closePopup2 = popup.find_element(By. ID, "closePopup2")
                        closePopup2.click()
                        logging.info("Popup закрыт")
                    except Exception:
                        logging.info("\u2705Popup2 был закрыт штатно")
                        continue  # Продолжаем цикл даже при ошибке

