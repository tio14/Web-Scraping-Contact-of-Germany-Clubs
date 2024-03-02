from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import pandas as pd

options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

url = "https://111bs.lions.de/unsere-clubs"
driver.get(url)
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[1]/section/div/div/div/div/div[4]/section/div/div/div/div/div/div/div[3]/div/button[2]").click()
close_popup = driver.find_element(By.XPATH, "/html/body/div[1]/section/div/div/div/div/div[3]/section/div/div/div/div[2]/div/div/div/div[1]/button/span")

district_list = []
founding_president_list = []
charter_date_list = []
president_list = []
club_meeting_list = []
club_website_list = []
club_email_list = []

club_list = driver.find_elements(By.CLASS_NAME, "club-entry")
for club in club_list:
    club.click()
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    district = soup.find("div", {"id": "districtValue"}).text
    district_list.append(district)
    founding_president = soup.find("div", {"id": "foundPresidentValue"}).text
    founding_president_list.append(founding_president)
    charter_date = soup.find("div", {"id": "charterDateValue"}).text
    charter_date_list.append(charter_date)
    president = soup.find("div", {"id": "presidentValue"}).text
    president_list.append(president)
    club_meeting = soup.find("div", {"id": "meetingPlacesValue"}).text
    club_meeting_list.append(club_meeting)
    club_website = soup.find("a", {"id": "websiteValue"}).text
    club_website_list.append(club_website)
    close_popup.click()

unsere_clubs_df = pd.DataFrame({"District": district_list,
                                "Founding President": founding_president_list,
                                "Charter Date": charter_date_list,
                                "President": president_list,
                                "Club Meeting": club_meeting_list,
                                "Club website": club_website_list})
unsere_clubs_df.to_csv("Unsere Clubs Contacts.csv")
