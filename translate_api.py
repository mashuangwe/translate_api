import pandas as pd
import os
import http.client
import hashlib
import urllib
import random
import json
import time

appid = 'xxxxx'  # 填写你的appid
secretKey = 'xxxxxxxxx'  # 填写你的密钥

httpClient = None

def baidu_translate(q, fromLang, toLang):
    salt = random.randint(32768, 65536)
    myurl = '/api/trans/vip/translate'
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        
#         print(result + '\n')
        return result
        
    except Exception as e:
        print(e)

    finally:
        if httpClient:
            httpClient.close()
            
fromLang = 'zh'  # 原文语种
toLang = 'en'  # 译文语种

def check_res(res):
    if res is None or \
        'trans_result' not in res or \
        len(res['trans_result']) == 0 or \
        'dst' not in res['trans_result'][0] or \
        res['trans_result'][0]['dst'] is None or \
        len(res['trans_result'][0]['dst']) == 0:
        return False
    return True
    
def total_translate(source_file, result_file):
    answer_dict = dict()
    with open(source_file, 'r', encoding='utf-8') as fr, \
        open(result_file, 'w', encoding='utf-8') as fw:
        start_time = time.time()
        for i, line in enumerate(fr):
            if (i + 1) % 10000 == 0:
                print(i + 1)
                print('use time:', time.time() - start_time)
                start_time = time.time()
            
            line = line.strip()
            if len(line) == 0:
                continue
            if line in answer_dict and answer_dict[line] != '':
                fw.write(answer_dict[line] + '\n')
                continue
            
            res = baidu_translate(line, fromLang, toLang)            
            if not check_res(res):
                fw.write('\n')
                continue
                
            line_en = res['trans_result'][0]['dst']
            q_zh = baidu_translate(line_en, toLang, fromLang)
            if not check_res(q_zh):
                fw.write('\n')
                continue
            
            line_zh = q_zh['trans_result'][0]['dst']
            answer_dict[line] = line_zh
            fw.write(line_zh + '\n')

            
if __name__ == '__main__':
    source_file = os.path.join(prefix, 'haha.txt')
    result_file = os.path.join(prefix, 'result.txt')
    total_translate(source_file, result_file)
    
    
