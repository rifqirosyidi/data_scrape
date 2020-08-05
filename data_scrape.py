from package.function import handle_elevenia, insert_and_get_fkey, export_to_excel
from package.config import my_db, my_cursor
import pyfiglet
from datetime import datetime
import time, sys, threading

list_cat = ['fashion', 'beauty', 'kids', 'home', 'food', 'gadget', 'elektronik', 'hobi', 'service']

ascii_banner = pyfiglet.figlet_format("Data Scraping.")
print(ascii_banner)
print("Extract and analyze data.")
print("-------------------------")

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


def your_function_name():
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
    headers = {'User-Agent': user_agent}

    url = 'https://elevenia.co.id/top100'

    top100 = handle_elevenia(url, headers)

    # Insert Date Scraping
    last_fkey = insert_and_get_fkey()

    my_cursor.executemany(f"""
        INSERT INTO data_product
            (id, title, link,  price, discount, review, rating, created_at)
        VALUES
            ('', %(title)s, %(link)s, %(price)s, %(discount)s, %(review)s, %(rating)s, {last_fkey})
    """, top100)

    my_db.commit()

    export_to_excel(top100)


def loadingAnimation(process):
    while process.isAlive():
        chars = "/—\|"
        for char in chars:
            sys.stdout.write('\r' + 'Extracting ' + char)
            time.sleep(.1)
            sys.stdout.flush()

    print('\nExtraction Successful\n')


loading_process = threading.Thread(target=your_function_name)
loading_process.start()
loadingAnimation(loading_process)
loading_process.join()