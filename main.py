from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Webdriver-Optionen festlegen
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')
options.add_argument('--window-size=1920x1080')

# Verwende WebDriverManager zum Installieren von ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Öffne die Webseite
    print("Öffne die Webseite...")
    driver.get("https://www.ligaportal.at/ooe/landesliga/landesliga-west/spieler-der-runde/105801-landesliga-west-waehle-den-beliebtesten-tipgame-com-spieler-der-saison-23-24")

    # Warte auf den iFrame des Cookie-Banners und wechsle hinein
    print("Warte auf den iFrame des Cookie-Banners...")
    cookie_iframe = WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='privacymanager.io']"))
    )

    # Akzeptiere die Cookies
    print("Akzeptiere die Cookies...")
    accept_cookies_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "save"))
    )
    accept_cookies_button.click()

    # Wechsle zurück zum Hauptinhalt
    driver.switch_to.default_content()

    # Warte ein paar Sekunden, um sicherzustellen, dass alles geladen ist
    print("Warte auf das Laden der Seite...")
    time.sleep(5)

    # Wechsel zum iframe, das das Voting-Formular enthält
    print("Wechsel zum iframe mit dem Voting-Formular...")
    voting_iframe = WebDriverWait(driver, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src*='iframe-loader-mk2.html']"))
    )

    # Versuche das Dropdown-Element zu finden
    print("Überprüfe, ob das Dropdown-Element vorhanden ist...")
    try:
        collapse_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-target='#collapse-64']"))
        )
        print("Element gefunden, scrolle und klicke darauf...")
        driver.execute_script("arguments[0].scrollIntoView(true);", collapse_button)
        collapse_button.click()
    except Exception as e:
        print("Fehler beim Finden des Elements:", e)
        driver.quit()
        exit()

    # Warte ein paar Sekunden, bis der Kollapsbereich geöffnet ist
    time.sleep(2)

    # Führe JavaScript aus, um den Radiobutton auszuwählen
    print("Wähle den Radiobutton per JavaScript aus...")
    script = """
    document.querySelector('input[id="voteItem-341568"]').checked = true;
    """
    driver.execute_script(script)

    # Warte ein paar Sekunden
    time.sleep(2)

    # Finde und klicke auf den Abstimmen-Button mit JavaScript
    print("Warte auf den Abstimmen-Button und klicke darauf...")
    submit_button_script = """
    document.querySelector('input[id="playerOneUp"]').click();
    """
    driver.execute_script(submit_button_script)

    print("Abstimmung erfolgreich abgeschlossen!")

finally:
    # Schließe den Webdriver
    print("Schließe den Webdriver...")
    driver.quit()
