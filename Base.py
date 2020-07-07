from time import sleep
from const import USER_AGENTS
from sys import stdout
from datetime import date, datetime
import time
from bs4 import BeautifulSoup
import requests
import logging
import logging.handlers
import os
import random
from lxml import html

class Base:

    def __init__(self):
        self.url = ''
        self.sleep=5
        self.logger = logging .getLogger()
        self.formatter = logging.Formatter(
            "%(asctime)s - %(thread)d - %(levelname)s - %(message)s"
        )
        self.scraper_type = ""
        self.status = True
        self.debug = False
        self.log = self.logger.info

    @staticmethod
    def get_content_simple(url: str, default_timeout: int = 10):
        user_agent = random.choice(USER_AGENTS)
        data = requests.get(
            url, headers={"User-Agent": user_agent}, timeout=default_timeout
        )
        time.sleep(random.randrange(5))
        return data
        # pickle.dump(data, file)

    # @staticmethod
    # def log(data):
    #     file = open(f"{os.getcwd()}/{datetime.now()}.html", 'w')
    #     print(data)
    #     file.write(data)

    def link_requestor(self, url: str):
        self.logger.info(f"Querying {url}")
        page = None
        self.status = False
        error = ""
        try:
            page = self.get_content_simple(url)
        except (
            requests.exceptions.MissingSchema,
            requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
        ):
            error = "Invalid url"
        except (
            requests.exceptions.SSLError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ChunkedEncodingError,
        ):
            error = "Either we are blocked by the server or internet is unstable!"
            sleep(self.sleep)
            try:
                self.logger.warning("Retrying")
                page = self.get_content_simple(url, default_timeout=60)
            except:
                error = "Its taking tooooooooooooooooooooo long to reconnect!"
            # finally:
            #     return page, error
        except Exception as e:
            self.logger.critical(e)
            error = "Unknown exception!"
        finally:
            if error:
                self.logger.error(f"{error} against {url}")
            else:
                page = BeautifulSoup(page.text, "html.parser")
                # page = html.fromstring(page.content)
                self.status = True

        return page

    def log_setup(self):
        self.logger.setLevel(logging.INFO)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        # file_name = f"{os.path.dirname(os.path.realpath(__file__))}/logs/{self.scraper_type}/{datetime.today()}"
        file_name = f"{os.path.dirname(os.path.realpath(__file__))}/logs/{self.scraper_type}/{datetime.now()}"
        handler = logging.handlers.TimedRotatingFileHandler(file_name)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        handler = logging.StreamHandler(stdout)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
