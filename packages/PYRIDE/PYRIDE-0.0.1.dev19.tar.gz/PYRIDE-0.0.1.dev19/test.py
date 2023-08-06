

from pyride.core import App
from pyride.pathway import path


def full():
    app = App(geometry='1400x600+250+200')

    ######################################################################
    app.env.add_page(text='Hello World', title='1')
    app.env.add_page(text='Money Time', title='2')
    file2 = path(r'C:\Users\Nick\Desktop\apartments.txt')
    app.env.add_page(file=file2, title='test')
    file1 = path(r'..\..\Utilities\DownloadTest\DigikeyAlumPolyCaps\html\1.html')
    app.env.add_page(file=file1, title='3')

    #app.env.insert_regex(r'href="((.*?)(?P<site>digikey).*?)"')
    app.env.insert_regex(r'href="(.*?)"')
    app.env.search()
    ######################################################################

    app.mainloop()
    app.quit()

def basic():
    app = App()
    app.mainloop()
    app.quit()


if __name__ == '__main__':
    full()
