import asyncio
from datetime import datetime
import configparser

import aiohttp
from aiopg.sa import create_engine
import bs4

from models import feed

config = configparser.ConfigParser(delimiters=(" ",))
config.read("config.ini")

DURATION = int(config['REQUESTS']['PERIOD'])

USER = config['POSTGRES']['user']
DB = config['POSTGRES']['db']
HOST = config['POSTGRES']['host']
PWD = config['POSTGRES']['password']


async def fetch(url):
    await asyncio.sleep(DURATION)
    async with aiohttp.request('GET', url) as resp:
        return await resp.text()


def parse(page):
    return bs4.BeautifulSoup(page, 'html.parser').find_all('item')


async def main(query):
    page = await fetch(query)
    data = parse(page)
    async with create_engine(user=USER,
                             database=DB,
                             host=HOST,
                             password=PWD) as engine:
        async with engine.acquire() as conn:
            for t in data:
                if t.find('title').string != None:
                    pd = t.find('pubdate').string.split(", ")[1][0:-4]
                    await conn.execute(
                        feed.insert().values(
                            title=t.find('title').string,
                            link=t.find('guid').string,
                            pub_date=datetime.strptime(pd, "%d %b %Y %H:%M:%S")
                        )
                    )


if __name__ == '__main__':
    URLS = [
        'http://rss.nytimes.com/services/xml/rss/nyt/Environment.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/ProBasketball.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/ProFootball.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Science.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Sports.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([main(u) for u in URLS]))
    loop.close()
