"""
Dziala dodawanie logow, wyswietlanie ich, wyswietlanie ostatnich 10 po osobie, wyswietlanie ostatnich 10 po kategorii

Zmienilem znak # na $, gdyz # powodowal problem

Nadal brakuje wyswietlania po czasie


Program ktory uruchamia serwer REST do obslugi eventow
W przegladarce nalezy wpisac:
http://localhost:8888/pushlog/LOGKTORYCHCEMYDODAC - aby dodac log, @OSOBA okresla do ktorej osoby jest log, $CATEGORY okresla dla jakiej kategorii jest lo
http://localhost:8888/showlogs - aby wyswietlic wszystkie logi
http://localhost:8888/showbyperson/OSOBY - w miejsce OSOBY wpisujemy, ktore logi do jakich osob chcemy wyswietlic na podstawie tego
                                            co wpisalismy przy dodawaniu loga, np. jesli przy dodawaniu wpisalismy @all to w miejsce OSOBY wpisujemy @all
                                            Zostanie wyswietlone tylko 10 ostatnich logow
http://localhost:8888/showcategory/CATEGORY - w miejsce CATEGORY wpisujemy, ktore logi do jakich kategorii chcemy wyswietlic na podstawie
                                            tego co wpisalismy przy dodawaniu loga, np. jesli przy dodawaniu wpisalismy $update to w miejsce CATEGORY
                                            wpisujemy $update
                                            Zostanie wyswietlone tylko 10 ostatnich logow
"""

import datetime
import json
import tornado.escape
import tornado.ioloop
import tornado.web


logs = []

"""
Zapisuje logi
"""
class PushLog(tornado.web.RequestHandler):
    def get(self, log):
        logs.reverse()
        logs.append(log)
        logs.reverse()
        liczba_logow = len(logs)
        self.write("Log " + json.dumps(log) + "zostal dodany. \nLiczba logow: " + json.dumps(liczba_logow))

"""
Wyswietla wszystkie logi
"""
class ShowLogs(tornado.web.RequestHandler):
    def get(self):
        dict = json.dumps(logs)
        self.write(dict)

"""
Wyswietla logi po osobie
"""
class ShowByPerson(tornado.web.RequestHandler):
    def get(self, person):
        persondict = {}
        x = 1
        if x < 10:
           for i in logs:
               if person in i:
                    persondict[x] = i
                    x += 1
        self.write(persondict)

"""
Wyswietla logi po kategorii
"""
class ShowByCategory(tornado.web.RequestHandler):
    def get(self, category):
        categorydict = {}
        x = 1
        if x < 10:
           for i in logs:
               if category in i:
                    categorydict[x] = i
                    x += 1
        self.write(categorydict)

application = tornado.web.Application([
    (r"/pushlog/(.*)", PushLog),
    (r"/showlogs", ShowLogs),
    (r"/showbyperson/(.*)", ShowByPerson),
    (r"/showbycategory/(.*)", ShowByCategory)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()