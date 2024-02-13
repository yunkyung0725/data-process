from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By

browser = webdriver.Chrome("")
browser.get("https://zigzag.kr/categories/-1?title=%EC%9D%98%EB%A5%98&category_id=-1&middle_category_id=436&sub_category_id=438&sort=201")
time.sleep(1)

html = browser.page_source
soup = BeautifulSoup(html, "html.parser")
zigzag_product_area = soup.select('.css-34da54.e91dh069')
result = []  # 상품 정보
result_review = []  # 상품 리뷰
for i in range(min(30,len(zigzag_product_area))):
    # 상품 정보
    a = zigzag_product_area[i]
    review = a.select_one('.css-1a9std3.e13zfay41').text
    review_num = a.select_one('.css-1lykwaz.e13zfay40').text
    review_num = ''.join(filter(str.isdigit, review_num))

    title = a.select_one('.CAPTION_12.REGULAR.css-4me7r9.e91dh064').text
    thumbnail = a.select_one('.css-1hlt7si.e81k49g0 > div > img').get('src')

    price = a.select_one('span.BODY_15.SEMIBOLD.css-1a86z8c.eh5ooyt0').text
    disc = a.select_one("span.BODY_15.SEMIBOLD.css-pd9h31.e91dh062")
    if disc:
        disc = disc.text
    else:
        disc = '할인 정보 없음'

    result.append([title, price, disc, review, review_num, thumbnail])


    # 상품 리뷰
    zigzag_post = soup.select(".css-1h2671j.e1dr6ufx0 > a")[i]
    zigzag_product_button = browser.find_element(By.CSS_SELECTOR, ".css-34da54.e91dh069")
    zigzag_product_button.click()

    browser.get("https://zigzag.kr/" + zigzag_post.get("href"))
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(1)

    zigzag_review = soup.select(".css-z61zy2.e9uiogx0")  # # #
    zigzag_review_text = soup.select_one(".swiper-wrapper")

    for j in range(min(5,len(zigzag_review))):
        review_name = zigzag_review[j].select_one(".BODY_16.SEMIBOLD.css-1k3hx0v.e1fnwskn0").text
        review_date = zigzag_review[j].select_one(".BODY_17.REGULAR.BODY_13.MEDIUM.css-1w6topb.e1cn5bmz0").text  # # #
        review_text = zigzag_review_text.select(".BODY_14.REGULAR.css-vqz6ex.e1unq90p2")[j].text
        result_review.append([review_name, review_date, review_text])
        #print(i, result_review[-1])

    browser.get("https://zigzag.kr/categories/-1?title=%EC%9D%98%EB%A5%98&category_id=-1&middle_category_id=436&sub_category_id=438&sort=201")
    time.sleep(1)

    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

# 상품 정보
df = pd.DataFrame(result, columns=['상품제목','가격','할인율','리뷰평점','리뷰개수','썸네일'])
df.to_csv('지그재그상품_크롤링_2조.csv', encoding='utf-8-sig')
print(df)

# 상품 리뷰
df_review = pd.DataFrame(result_review, columns=['리뷰어', '리뷰 날짜', '리뷰 텍스트'])
df_review.to_csv("지그재그리뷰_크롤링_2조.csv", encoding="utf-8-sig")
print(df_review)