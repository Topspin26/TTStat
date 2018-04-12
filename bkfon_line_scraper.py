import psycopg2
import config as config
from BKFonLiveScraper import (
    BKFonFileWriter,
    BKFonDBWriter,
    BKFonScraperEngine
)
from driver import Driver


def main():

    con = None
    driver = None
    try:
        con = psycopg2.connect(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )

        file_writer = BKFonFileWriter('data_fonbet_line')
        db_writer = BKFonDBWriter(con, 'fonbet_line')

        driver = Driver('chrome')

        scraper_engine = BKFonScraperEngine(
            'https://www.fonbet.ru/#/bets',
            driver=driver,
            file_writer=file_writer,
            db_writer=db_writer,
            sport='3088',
            active_timeout=5 * 60,
            passive_timeout=5 * 60
        )
        scraper_engine.run()

    finally:
        if con:
            con.close()
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
