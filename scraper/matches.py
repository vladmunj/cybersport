from app.config import (MINIO_EVENTS_BUCKET_NAME, BASE_URL,
                        MINIO_MATCHES_BUCKET_NAME)
from services.minio_client import MinioClient
from scraper.events import events_object_name
import requests as req
from bs4 import BeautifulSoup as bs
from datetime import datetime

MATCHES_CLASS_VALUE="battleRoyale_"

def matches_object_name(event_title, date, match_name):
    object_date = datetime.now().strftime('%Y-%m-%d')
    return f"{object_date}/{event_title}/{date}/{match_name}.json"

events_object_name = events_object_name()
minio_client = MinioClient()
events = minio_client.get_json(MINIO_EVENTS_BUCKET_NAME, events_object_name)
for event in events:
    response = req.get(event['link'])
    soup = bs(response.text, 'html.parser')
    matches = soup.select(f'[class*="{MATCHES_CLASS_VALUE}"]')
    for match in matches:
        date = match.select_one('[class^="date_"]').text
        team1 = match.select_one(
            '[class*="participant1_"] [class^="titleWrapper_"] [class^="title_"]'
        ).text
        team2 = match.select_one(
            '[class*="participant2_"] [class^="titleWrapper_"] [class^="title_"]'
        ).text
        score_block = match.select_one('[class^="score_"]')
        score = ''.join(
            value.get_text(strip=True)
            for value in score_block.select('span')
        )
        link = (BASE_URL.rstrip('/') + '/'
                + match.select_one('[class^="matchLink_"]').attrs['href'].lstrip('/'))
        matches_data = {
            'date': date,
            'team1': team1,
            'team2': team2,
            'score': score,
            'link': link,
            'title': event['title']
        }
        object_name_date = (datetime
                            .strptime(date, '%d.%m.%y в %H:%M')
                            .strftime('%Y-%m-%d'))
        match_object_name = matches_object_name(
            event['title'].replace(' ','_'),
            object_name_date,
            team1 + "_vs_" + team2
        )
        minio_client.upload_json(
            MINIO_MATCHES_BUCKET_NAME,
            matches_data,
            match_object_name
        )