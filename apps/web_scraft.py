# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time
#
# service = Service(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
#
# driver.get('https://uzum.uz/uz/category/hafta-tovarlari--895')
# wait = WebDriverWait(driver, 15)
# wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))
#
# cards = driver.find_elements(By.CSS_SELECTOR, ".product-card")
# products = []
#
# for card in cards:
#     try:
#         title = card.find_element(By.CSS_SELECTOR, '.product-card__title').text
#         price = card.find_element(By.CSS_SELECTOR, '[data-test-id="product-card__actual-price"]').text
#
#         card.click()
#         time.sleep(3)
#         detail_url = driver.current_url
#
#         try:
#             order_info = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="text__product-banner"]')[1].text
#         except:
#             order_info = "Ma'lumot yo'q"
#
#         driver.back()
#         time.sleep(2)
#
#         products.append({
#             'title': title,
#             'price': price,
#             'orders': order_info,
#             'url': detail_url
#         })
#     except Exception as e:
#         products.append("Noma'lum")
#
# print(products)
#
# driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# import time
#
# option = webdriver.ChromeOptions()
# # options.add_argument('--headless')
# option.add_argument('--incognito')
# option.add_argument('--ignore-certificate-errors')
# option.add_argument('window-size=1000,800')
# option.add_argument('--disable-cache')
# service = Service(executable_path=ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=option)
#
# driver.get('https://uzum.uz/uz/category/hafta-tovarlari--895')
# wait = WebDriverWait(driver, 15, poll_frequency=1)
# products_path = (By.XPATH, "//a[contains(@class, 'product-card')]")
# cards = wait.until(EC.presence_of_all_elements_located(products_path))
# products = []
# for card in cards:
#     title = card.find_element(By.XPATH, "//div[@class='product-card__title']").text
#     by_card_price = card.find_element(By.XPATH, "//span[@class='currency']").text
#     price = card.find_element(By.XPATH, "//span[contains(@class, 'card-price__regular')]").text
#
#     products.append({
#         "title": title,
#         "by_card_price": by_card_price,
#         "price": price
#     })
# print(products)
