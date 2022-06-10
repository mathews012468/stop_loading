import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

def is_cookie_message_visible(driver):
    """specific to nytimes articles"""
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup.find(attrs={"data-testid": "gdpr-dock"}) != None

def wait_until_cookie_message_is_visible(driver, timeout=1):
    start_time = time.time()
    while True:
        now = time.time()
        time_since_function_started = now - start_time
        if is_cookie_message_visible(driver) or time_since_function_started > timeout:
            #give it some more time
            time.sleep(2)
            break

def make_cookie_message_disappear(driver):
    cookie_element = driver.find_element(By.XPATH, "//div[@data-testid='gdpr-dock']")
    driver.execute_script("arguments[0].setAttribute('style', 'visibility: hidden')", cookie_element)

def allow_scrolling(driver):
    main_element = driver.find_element(By.NAME, "main")
    driver.execute_script("arguments[0].setAttribute('style', 'position: relative')", main_element)

def stop_loading_after_seconds(url, load_time=0.5):
    """
    url: string, link
    load_time: seconds, page will be allowed to load for load_time seconds
    """
    #set up driver to return as soon as possible (before the ads kick in)
    options = Options()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_experimental_option("detach", True)
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)

    print(1)

    driver.get(url)

    print(2)

    time.sleep(load_time)

    print(3)
    
    driver.execute_script("window.stop();")

    print(4)

    wait_until_cookie_message_is_visible(driver)

    print(5)

    if is_cookie_message_visible(driver):
        make_cookie_message_disappear(driver)

    print(6)

    allow_scrolling(driver)

    print(7)

    #TEST
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # title = soup.find("h1").text
    # with open(title + ".html", "w") as articleWriter:
    #     articleWriter.write( soup.__str__() )

    return soup.__str__()


if __name__ == "__main__":
    url = input("Enter url of NYTimes article: ")
    load_time = input("Enter load time: ")

    load_time = float(load_time)
    stop_loading_after_seconds(url, load_time)


# height = driver.execute_script("return window.innerHeight")
# driver.save_screenshot("part0.png")
# #TEST
# for i in range(1, 10):
#     print( is_cookie_message_visible(driver) )
#     webdriver.ActionChains(driver).scroll_by_amount(0, int(height * 0.75)).perform()
#     driver.save_screenshot(f"part{i}.png")

#1. wait until cookie message is visible
#2. get rid of cookie message
#3. screenshot the entire page

#take screenshots of entire page
#https://stackoverflow.com/questions/3422262/how-can-i-take-a-screenshot-with-selenium-webdriver

# #https://stackoverflow.com/questions/43734797/page-load-strategy-for-chrome-driver-updated-till-selenium-v3-12-0
# options = Options()
# options.page_load_strategy = 'eager'
# driver = webdriver.Chrome(options=options)

# url = "https://www.nytimes.com/1994/11/13/nyregion/left-to-die-the-south-bronx-rises-from-decades-of-decay.html"
# driver.get(url)

# time.sleep(0.5)
# driver.execute_script("window.stop();")
# stop_loading_after_seconds(url)
