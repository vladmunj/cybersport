import requests as req
from services.alert import report
from requests.exceptions import HTTPError
from app.config import HTTP_TIMEOUT_SECONDS

def http_req(url):
    try:
        response = req.get(
            url,
            timeout = HTTP_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response
    except HTTPError as err:
        report(err)
    except Exception as err:
        report(err)