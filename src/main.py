from collector.batdongsan.batdongsanContext import BatDongSanContext


context = BatDongSanContext(url='https://batdongsan.com.vn/ban-can-ho-chung-cu-goldsilk-complex')

context.crawlSalePostUrls()
context.excuteCrawl()









# # Sale list
# sales = []

# for url in lst:
#     try: 
#         url_new = url.replace('http://localhost:3000','http://localhost:3000/?cmd=get&path=https://batdongsan.com.vn')
#         driver.get(url_new)

#         # Get name
#         nameElement = driver.find_elements(By.CSS_SELECTOR, "div.re__contact-name.js_contact-name")[0]
#         name = nameElement.get_attribute('title')
        
#         # Get phone raw
#         phoneElement = driver.find_elements(By.CSS_SELECTOR, 'div.phone.js__phone')[0]
#         phone_raw = phoneElement.get_attribute('raw')

#         # Call API to decrypt phone raw
#         url_crawl_phone = "https://batdongsan.com.vn/Product/ProductDetail/DecryptPhone"
#         driver.get(f"http://localhost:3000/?path={url_crawl_phone}&postData=PhoneNumber={phone_raw}&cmd=post")

#         # Get phone
#         phone_number = driver.find_elements(By.CSS_SELECTOR, 'pre')[0].get_attribute('innerHTML')
#         phone_number = re.sub(r'\s', '', phone_number)

#         sales.append({
#             'name': name, 
#             'phone': phone_number
#         })

#         print("Crawl success: " + url_new)
#     except Exception as ex:
#         print("Crawl failure: " + url_new)
#         print(ex)


# # Insert sale data to database
# requests.post(f"http://localhost:3000/user/bulk", json={'users': sales})

