"""Selenium UI tests for the CI/CD Assignment 3 site (Harris Ahmad, FA23-BCT-012)."""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = os.environ.get("BASE_URL", "http://cicd-012-staging")
TIMEOUT = 10

NAME = "Harris Ahmad"
ROLL = "FA23-BCT-012"


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    for flag in (
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1280,800",
        "--user-data-dir=/tmp/chrome-profile",
    ):
        options.add_argument(flag)
    drv = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
    yield drv
    drv.quit()


def open_site(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "heading"))
    )


def test_title_contains_roll_number(driver):
    open_site(driver)
    WebDriverWait(driver, TIMEOUT).until(EC.title_contains(ROLL))
    assert ROLL in driver.title


def test_heading_shows_name(driver):
    open_site(driver)
    heading = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "heading"))
    )
    assert heading.text.strip() == NAME


def test_roll_number_displayed(driver):
    open_site(driver)
    roll = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "roll"))
    )
    assert roll.text.strip() == f"Roll No: {ROLL}"


def test_button_click_shows_message(driver):
    open_site(driver)
    WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "msgBtn"))
    ).click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.ID, "message"), "Hello")
    )
    message = driver.find_element(By.ID, "message").text
    assert NAME in message


def test_textbox_submit_displays_text(driver):
    open_site(driver)
    sample = "Selenium says hi from FA23-BCT-012"
    box = WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "textInput"))
    )
    box.clear()
    box.send_keys(sample)
    driver.find_element(By.ID, "submitBtn").click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.text_to_be_present_in_element((By.ID, "output"), sample)
    )
    assert driver.find_element(By.ID, "output").text == f"You entered: {sample}"
    driver.save_screenshot("screenshot.png")
