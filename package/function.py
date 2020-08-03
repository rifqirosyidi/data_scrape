from lxml import html
import requests
import pandas as pd
from requests import ConnectionError
from package.config import my_cursor, my_db
from datetime import datetime


def export_to_excel(products, file_name="products.xlsx"):
    df = pd.DataFrame.from_dict(products)
    df.to_excel(file_name)


def handle_elevenia(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    product_list = tree.xpath('//div[@id="product_listing"]//div[@class="group"]')

    top100 = []
    for product in product_list:
        titles = product.xpath('a[@class="pordLink notranslate"]/text()')
        prices = product.xpath('div[@class="price notranslate"]/strong/text()')
        discounts = product.xpath('div[@class="price notranslate"]/span/text()|'
                                  'div[@class="price notranslate"][not(span)]/text()')
        reviews = product.xpath('div[@class="rankingArea"]/span/em/a/text()[1]|'
                                'div[@class="rankingArea"][not(span/em/a/text())]')
        ratings = product.xpath('div[@class="rankingArea"]/span/@class | div[@class="rankingArea"][not(span/@class)]')

        for title, price, discount, review, rating in zip(titles, prices, discounts, reviews, ratings):
            if discount == "\t":
                discount = ""
            top100.append({'title': title,
                           'price': price,
                           'discount': discount,
                           'review': review,
                           'rating': rating
                           })

    for top in top100:
        # Cleaning Review
        top['review'] = str(top['review']).replace("(", "").strip()
        if not top['review'].isdigit():
            top['review'] = ''

        top['rating'] = str(top['rating'])[-1].replace(">", "").strip()

    # Insert The Date Scraped
    now = datetime.now()
    sql_query = 'INSERT INTO date_scrape (id, created_at) VALUES (%s, %s)'
    sql_value = ('', now.strftime('%Y-%m-%d %H:%M:%S'))
    my_cursor.execute(sql_query, sql_value)
    last_foreign_key_val = my_cursor.lastrowid
    my_db.commit()
    print(my_cursor.rowcount, "record inserted.")

    my_cursor.executemany(f"""
        INSERT INTO data_product (id, title, price, discount, review, rating, created_at)
        VALUES ('', %(title)s, %(price)s, %(discount)s, %(review)s, %(rating)s, {last_foreign_key_val})
    """, top100)

    print('DATA INSERTED: ', my_cursor.rowcount, 'data')
    my_db.commit()

    export_to_excel(top100)


