# A simple wrapper of requests

## Installation
```bash
pip install webrequests
```

## Usage
```python
from webrequests import WebRequest


url = 'http://output.nsfc.gov.cn/captcha/defaultCaptcha'

# request an url
resp = WebRequst.get_response(url)
resp = WebRequst.get_response(url, method='POST', max_try=5, timeout=5)
print(resp.headers)


# download file from an url
WebRequst.download(url, 'out.jpg')
WebRequst.download(url, 'out.jpg', max_try=5, timeout=10)


# request with session
import requests

session = requests.session()
resp = WebRequst.get_response(url, session=session)
print(resp.cookies)
print(session.cookies)


# get a soup
url = 'http://www.cip.cc/'
soup = WebRequst.get_soup(url)
print(soup.select_one('.kq-well pre').text.strip())
```
