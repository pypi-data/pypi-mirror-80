
import requests, traceback


IDENTITY = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    }


#FIX THE BROKEN TIMEOUT STATEMENT
def download(url, *, params=None, header=IDENTITY, timeout=5000,
             save=False, from_cache=False):
    """
        All times are in ms, all data is in Kb

        What if we dont want to raise an error after all retries have been exhausted

        What about the ability to pass a checking function into the req.ok if-statement
            Has to retry if theres a connection issue
            ALSO has to retry if the data isnt good !
    """
    try:
        req = requests.get(url, params=params, headers=header, timeout=timeout/1000)
        req.raise_for_status()
    except Exception as error:
        return traceback.format_exc(), False # The 'False' signifies an error

    
    #html_bytes = req.content
    html_text = req.text
    size = len(html_text) / 1000

    if save:
        filename = path(name=directoryify(full_url), ext='html')
        with open(filename, 'wb') as handle:
            handle.write(html_bytes)

    return html_text, True # The 'True' signifies a success

if __name__ == '__main__':
    url = r'https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Separator.html'
    html = download(url)
    print(html)