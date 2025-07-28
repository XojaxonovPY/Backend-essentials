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