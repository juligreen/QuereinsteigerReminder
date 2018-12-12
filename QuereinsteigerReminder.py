import traceback
import requests
import schedule
import time
from bs4 import BeautifulSoup
import telegram

import ini_parser


class Reminder:
    counter = 0

    @staticmethod
    def send(msg):
        bot = telegram.Bot(token=ini_parser.get_telegram_token())
        bot.sendMessage(chat_id=ini_parser.get_telegram_chat_id(), text=msg)

    def job(self):
        self.counter += 1
        print(f"{self.counter}. run since start")
        page = requests.get("https://www.km.bayern.de/lehrer/lehrerausbildung/gymnasium/quereinstieg.html")
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            if 'informatik' in soup.prettify().lower():
                self.send("Quereinsteiger für Informatik (Gymnasium) vorhanden!")
        else:
            self.send("Kultusministerium Seite down oder Probleme bei der Abfrage")


if __name__ == "__main__":
    reminder = Reminder()
    schedule.every().day.at("14:00").do(reminder.job)

    while True:
        try:
            schedule.run_pending()
        except Exception:
            time.sleep(60)
            my_stacktrace = traceback.format_exc()
            if len(my_stacktrace) < 4090:
                reminder.send(my_stacktrace)
            else:
                reminder.send(my_stacktrace[:4090])
                reminder.send(my_stacktrace[4090:8180])
            print(traceback.format_exc())
        time.sleep(60)
