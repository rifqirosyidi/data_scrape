from package.function import handle_elevenia


user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0'
headers = {'User-Agent': user_agent}

url = 'https://elevenia.co.id/top100'

handle_elevenia(url, headers)
