import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

driver = webdriver.Chrome()


def extract_reviews(number, product_link):

    # Every product my not contain more number of reviews so we discard the less number of reviews
    if number > 10:
        driver.get(product_link)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        name = soup.find("span", class_="VU-ZEz").text
        print("Loading data of " + name)
        rating_span = soup.find("span", class_="Wphh3N")

        anchor_tag = soup.find("div", class_="col pPAw9M").find("a")
        href_value = anchor_tag["href"]
        l = "https://www.flipkart.com" + href_value
        # print(l)
        driver.get(l)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        anchor_tag = soup.find("div", class_="+uoMff").find("a")
        href_value = anchor_tag["href"]
        li = "https://www.flipkart.com" + href_value
        # print(li)
        driver.get(li)

        head = []
        desc = []
        cus_name = []
        place = []
        R_date = []

        def extract_reviews_for_sort(sort_option):
            try:
                sort_filter = Select(
                    driver.find_element(By.CSS_SELECTOR, ".OZuttk.JEZ5ey")
                )
                sort_filter.select_by_value(sort_option)
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, "html.parser")
                anchor_tag = soup.find("a", class_="_9QVEpD")
                href_value = anchor_tag["href"]
                l = "https://www.flipkart.com" + href_value
                # print(l)
                F_url = []

                end_index = l.rfind("=") - 1
                new_url = l[: end_index + 1]
                n = int(number / 10)
                # classifying the number of pages needed to be scrape.
                if n >= 20:
                    num = 10
                elif n <= 19 and n >= 11:
                    num = 8
                elif n <= 10 and n >= 7:
                    num = 7
                elif n <= 6 and n >= 10:
                    num = 5
                elif n <= 5 and n >= 3:
                    num = 3
                elif n == 2 or n == 1:
                    num = 1
                else:
                    num = False
                if num:
                    for i in range(1, num - 1):

                        link = str(new_url + "=" + str(i))
                        F_url.append(link)

                    for i in F_url:
                        driver.get(i)
                        html_content = driver.page_source
                        soup = BeautifulSoup(html_content, "html.parser")

                        reviews = soup.find_all("div", class_="col EPCmJX Ma1fCG")

                        for review in reviews:
                            customer_name = review.find("p", class_="_2NsDsF AwS1CA")
                            name = customer_name.text.strip()
                            if customer_name:
                                cus_name.append(name)

                            else:
                                cus_name.append("NIL")

                            rating_element = review.find("div", class_="ZmyHeo")
                            rating = rating_element.text.strip()
                            if rating_element:
                                desc.append(rating)

                            else:
                                desc.append("NIL")

                            review_text_element = review.find("p", class_="z9E0IG")
                            review_text = review_text_element.text.strip()
                            if review_text_element:
                                head.append(review_text)
                            else:
                                head.append("NIL")

                            id_span = review.find("p", class_="MztJPv")
                            if id_span:
                                spans = id_span.find_all("span")
                                location = spans[1].text.strip()
                                if not location:
                                    place.append("NIL")
                                place.append(location)
                            else:
                                place.append("NIL")
                        print(len(place))
            except Exception as E:
                print("Didn't work")

        sort_options = ["POSITIVE_FIRST", "NEGATIVE_FIRST"]
        for sort_option in sort_options:
            extract_reviews_for_sort(sort_option)
        print(len(head))
        print(len(desc))
        print(len(cus_name))
        print(len(place))
        df = pd.DataFrame(
            {"Heading": head, "Description": desc, "Name": cus_name, "Place": place}
        )
        if "\xa0\xa0" in name:
            name = name.split("|")[0].strip()
        csv_file_path = os.path.join("data", str(name) + ".csv")
        df.to_csv(csv_file_path, index=False)


# I used a group of link in a CSV file to collect group of data
df = pd.read_csv("link2.csv")
for index, row in df.iterrows():
    product_link = row["Link"]
    review_data = row["reviews"]
    extract_reviews(review_data, product_link)

"""Example: 517,https://www.flipkart.com/motorola-g04s-satin-blue-64-gb/p/itma899ac4728c8e?pid=MOBHY9PQM9H8HMEN&lid=LSTMOBHY9PQM9H8HMENQJT1JU&marketplace=FLIPKART&q=mobile&store=tyy%2F4io&srno=s_2_29&otracker=AS_Query_OrganicAutoSuggest_4_2_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_4_2_na_na_na&fm=organic&iid=d67ff0de-936b-4735-9a4f-5e428c1ed8f7.MOBHY9PQM9H8HMEN.SEARCH&ppt=None&ppn=None&ssid=rdrwipk0680000001722740530447&qH=532c28d5412dd75b
"""
