import requests
import logging
import httplib

class CustomHttpClient:

  def __init__(self, log=True):
    if log:
      self.setup_logging()

  def setup_logging(self):
    httplib.HTTPSConnection.debuglevel = 2

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

  def get(self, url, params={}):
    response = requests.get(url, json=params)
    return self.log_response(response)

  def post(self, url, params):
    response = requests.post(url, json=params)
    return self.log_response(response)

  def delete(self, url):
    response = requests.delete(url)
    return self.log_response(response)

  def log_response(self, response):
    print 'DEBUG:client.http_client:response body\n' + response.text + '\n'
    return response

