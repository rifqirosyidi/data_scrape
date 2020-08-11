from package.function import handle_elevenia, insert_and_get_fkey, loading_animation
from package.config import my_db, my_cursor
import pyfiglet
from datetime import datetime
import threading

list_cat = ['fashion', 'beauty', 'kids', 'home', 'food', 'gadget', 'elektronik', 'hobi', 'service']

ascii_banner = pyfiglet.figlet_format("Data Scraping.")
print(ascii_banner)
print("Extract and analyze data.")
print("-------------------------")
print("Do You Want To Extract Or Analyze Data? \nEnter 'e' for Extract, 'a' for Analyse..")

while True:

    data_mode = str(input()).lower()
    if data_mode == 'a' or data_mode == 'e':
        break
    else:
        print("Please Enter E or A")
        continue

print("List of category : ", end="")
print(*list_cat, sep=", ")

category = str(input("Please Enter Category (Skip to Default): ")).lower()
if category == "":
    category = ""
elif category in list_cat:
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : Extracting... {category.capitalize()}\n")
else:
    print("Error")
    exit()


def analyze_data():
    pass


def extract_data():
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    headers = {'User-Agent': user_agent}
    global category

    if category != "":
        url = f'https://elevenia.co.id/top100-{category}'
    else:
        url = 'https://elevenia.co.id/top100'
        category = "all"

    top100 = handle_elevenia(url, category, headers)

    # Insert Date Scraping
    last_fkey = insert_and_get_fkey()

    my_cursor.executemany(f"""
        INSERT INTO data_product
            (id, title, link,  price, discount, review, rating, category, created_at)
        VALUES
            ('', %(title)s, %(link)s, %(price)s, %(discount)s, %(review)s, %(rating)s, %(category)s, {last_fkey})
    """, top100)

    my_db.commit()
    print('\nExtraction Successful\n')


loading_process = threading.Thread(target=extract_data)
loading_process.start()
loading_animation(loading_process)
loading_process.join()
