import psycopg2
import config as config
from BKFonLiveScraper import (
    BKFonFileWriter,
    BKFonDBWriter,
    BKFonScraperEngine
)


def main():

    con = None
    scraper_engine = None
    try:
        con = psycopg2.connect(
            host=config.DB_HOST,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )

        file_writer = BKFonFileWriter('data_fonbet_live')
        db_writer = BKFonDBWriter(con, 'fonbet_live')
        scraper_engine = BKFonScraperEngine(
            'https://www.fonbet.ru/#/live',
            file_writer=file_writer,
            sport='3088',
            db_writer=db_writer,
            active_timeout=5,
            passive_timeout=60
        )
        scraper_engine.run()

    finally:
        if con:
            con.close()
        if scraper_engine.driver:
            scraper_engine.driver.quit()


if __name__ == "__main__":
    main()