import requests as req
from requests.exceptions import HTTPError, RequestException
from app.config import HTTP_TIMEOUT_SECONDS
from exceptions.http import HttpException

def http_req(url):
    try:
        response = req.get(
            url,
            timeout = HTTP_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response
    except HTTPError as err:
        raise HttpException(err) from err
    except Exception as err:
        raise HttpException(err) from err
    except RequestException as err:
        raise HttpException(err) from err