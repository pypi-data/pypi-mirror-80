import json
import requests


def dic_to_json(dic1):
    return json.dumps(dic1)


if __name__ == '__main__':
    headers = {'appTypeEnum':'3','userAccountType':'3','loginType':'1','overLayFlag':'2','platform':'ANDROID'}
    dic1 = {"userName": "13540424181", "password": "a8fbf432533529eae1b4f8bb37178373", "checkType": "0", "deviceType": 1}
    d2 = dic_to_json(dic1)
    dic2 = {"param":d2}
    r = requests.post("http://testopen.dmall.com/app/login", data=dic2,headers=headers)
    print(r.content)