import threading
import aiohttp
import json

class Requests(threading.Thread):

    async def requestAction(self, requestDatas):
        url="http://localhost:8080/test3"
        json_string=json.dumps(requestDatas)
        print(json_string)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        async with aiohttp.ClientSession() as session:
            async with session.post(url,headers=headers,data=json_string) as resp:
                data = await resp.text()
                print(data)



