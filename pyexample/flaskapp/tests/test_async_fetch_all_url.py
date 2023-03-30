from app.views import async_fetch_all_url
from requests import Response
import json
from .data.async_fetch_all_url_data import text_data,dict_data


def test_bytediff_async_fetch_all_url():
    result = async_fetch_all_url(text_from="2",request_data=dict_data)
    assert isinstance(result.get('prod'),Response) and isinstance(result.get('ppe_douplus_new'),Response)


def test_bytest_async_fetch_all_url():
    import re
    regex = re.compile("'request': '(.*?)',")
    request_text = regex.findall(text_data)[0]
    request_data = json.loads(request_text)

    result = async_fetch_all_url(text_from="1",request_data=request_data)
    assert isinstance(result.get('prod'),Response) and isinstance(result.get('ppe_douplus_new'),Response)






