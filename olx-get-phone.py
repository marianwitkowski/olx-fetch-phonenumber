import requests
import sys
import json

def find_access_token(har):
    access_token, user_id, offer_id, user_cookies = (None,)*4
    entries = har.get("log",{}).get("entries",[])
    if len(entries)==0: return (access_token, user_id, offer_id, user_cookies)
    for entry in entries:
        if access_token and user_id:
            break
        cookies = entry.get("request",{}).get("cookies",[])
        for cookie in cookies:
            if cookie.get("name") == "a_access_token":
                access_token =  cookie.get("value")
            if cookie.get("name") == "user_id":
                user_id =  cookie.get("value")
            if access_token and user_id:
                user_cookies = cookies
                break

    for entry in entries:
        if offer_id: break
        qss = entry.get("request",{}).get("queryString",[])
        for qs in qss:
            if qs.get("name") == "ad_id":
                offer_id = qs.get("value")
                break

    return access_token, user_id, offer_id, user_cookies

###############################

def generate_challenge(user_id):
    headers = {
        'authority': 'friction.olxgroup.com',
        'accept': '*/*',
        'accept-language': 'pl,en;q=0.9,en-US;q=0.8,pl-PL;q=0.7',
        'origin': 'https://www.olx.pl',
        'referer': 'https://www.olx.pl/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-user-tests': 'eyJidXktMjcxMiI6ImIiLCJjYXJzLTMxODc1IjoiYiIsImNhcnMtMzQ0NTQiOiJhIiwiY2Fycy0zNDQ1NSI6ImEiLCJjYXJzLTM1MDk3IjoiYSIsImNhcnMtMzUyNzIiOiJiIiwiZXItMTcwOCI6ImEiLCJlci0xNzI1IjoiYSIsImVyLTE3NzgiOiJiIiwiZXJtLTc5NiI6ImQiLCJmOG5ycC0xMTgzIjoiYiIsImpvYnMtMzQ4MiI6ImEiLCJqb2JzLTM3MTciOiJjIiwiam9icy0zNzIyIjoiYSIsImpvYnMtMzcyOCI6ImIiLCJqb2JzLTM4MzciOiJjIiwiam9icy00MDIzIjoiYiIsIm9lc3gtMTU0NyI6ImEiLCJvZXN4LTE4MDMiOiJiIiwib2V1MnUtMjMyMyI6ImIifQ==',
    }

    json_data = {
        'action': 'reveal_phone_number',
        'aud': 'atlas',
        'actor': {
            'username': str(user_id),
        },
        'scene': {
            'origin': 'olx.pl',
        },
    }

    response = requests.post('https://friction.olxgroup.com/challenge', headers=headers, json=json_data)
    return response.json()

###############################

def generate_exchange(challenge):
    headers = {
        'authority': 'friction.olxgroup.com',
        'accept': '*/*',
        'accept-language': 'pl,en;q=0.9,en-US;q=0.8,pl-PL;q=0.7',
        'origin': 'https://www.olx.pl',
        'referer': 'https://www.olx.pl/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    json_data = {
        'context': challenge.get("context"),
        'response': '',
    }

    response = requests.post('https://friction.olxgroup.com/exchange', headers=headers, json=json_data)
    return response.json()

###############################

def fetch_phone(exchange, offer_id, access_token):
    cookies = {
        'mobile_default': 'desktop',
        'lister_lifecycle': '1662624080',
        'fingerprint': 'MTI1NzY4MzI5MTs4OzA7MDswOzE7MDswOzA7MDswOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTswOzE7MTsxOzE7MDswOzA7MDswOzA7MTsxOzE7MTsxOzA7MTswOzA7MTsxOzE7MDswOzA7MDswOzA7MDswOzE7MDswOzA7MDsxOzE7MDsxOzE7MDsxOzE7MTsxOzA7MTswOzM5NTA5MTEyNjQ7MjsyOzI7MjsyOzI7NTsyODQ4MDA2NDE4OzEzNTcwNDE3Mzg7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzE7MTsxOzA7MDswOzE1OTA4MjQyNjQ7MzQ2OTMwNjU1MTszNzgyNjU5MDMwOzc4NTI0NzAyOTszOTU1NDQ4NjkzOzE0NDA7OTAwOzMwOzMwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDsxMjA7NjA7MTIwOzYwOzEyMDs2MDswOzA7MA==',
        'dfp_user_id': 'eeb7c01d-f66b-424a-952d-700f2c29230d-ver2',
        'from_detail': '0',
        'ldTd': 'true',
        'laquesissu': '298@reply_chat_sent|1#302@jobs_applications|0',
        'user_adblock_status': 'true',
        'OptanonAlertBoxClosed': '2022-09-08T08:01:22.908Z',
        'eupubconsent-v2': 'CPfAE0rPfAE0rAcABBENCfCsAP_AAH_AAAYgI_Nf_X__b2_j-_5_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVryPsbk2cr7NKJ7PEmnMbOydYGH9_n1_z-ZKY7_____7z_v-v___3____7-3f3__p_3_-__e_V_99zfn9_____9vP___9v-_9__________3_79BH0Akw1biALsSxwJtowigRAjCsJDqBQAUUAwtEBhA6uCnZXAT6whYAIBQBGBECHEFGDAIAAAIAkIiAkCPBAIgCIBAACABUAhAARsAgoALAwCAAUA0LFGKAIQJCDIgIilMCAiRIKCeyoQSg70NMIQ6ywAoNH_FQgIlACFYEQkLByHBEgJeLJAsxRvkAIwQoBRKhQAAA.f_gAD_gAAAAA',
        'OTAdditionalConsentString': '1~89.2008.2072.2322.2465.2501.2999.3028.3225.3226.3231.3232.3234.3235.3236.3237.3238.3240.3241.3244.3245.3250.3251.3253.3257.3260.3268.3270.3272.3281.3288.3290.3292.3293.3295.3296.3300.3306.3307.3308.3314.3315.3316',
        'newrelicInited': '0',
        '__utmc': '221885126',
        '__utmz': '221885126.1662624083.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '__utma': '221885126.50322128.1662624083.1662624083.1662624083.1',
        '_gid': 'GA1.2.1255599002.1662624083',
        '_gcl_au': '1.1.620311010.1662624083',
        '__gfp_64b': '3mBreyjEzOGDxcx3_kBwZf6ja3ZbmAVFZPNqQlS_Zmf.W7|1662624083',
        '_hjSessionUser_1685071': 'eyJpZCI6ImQ5NTU4Mzk3LTc2ZGUtNWY5MC04YTEyLTU4MjYxYTQ1MTA3YiIsImNyZWF0ZWQiOjE2NjI2MjQwODE0NTAsImV4aXN0aW5nIjp0cnVlfQ==',
        'deviceGUID': '71a523b6-0423-4660-9dc2-432dd10fd918',
        '__gsas': 'ID=78393521b654300e:T=1662624095:S=ALNI_MbFjGZ93jDYelSfNJroAK-z9dF8VA',
        '__gads': 'ID=8b04f01c10ff4676-224d30d017ce0005:T=1662624127:RT=1662624127:S=ALNI_MYhMnKVcCMyeRu7qYrPci7NgZE_fQ',
        'observed_aui': '2d73969bbc54499aab9359a41a1df9bb',
        'a_access_token': access_token,
        'a_refresh_token': 'd8cb13baa2908118eb3661073ed8f9af2a441dcc',
        'a_grant_type': 'device',
        'user_id': '1311015425',
        'user_business_status': 'private',
        'laquesis': 'buy-2712@b#cars-31875@b#cars-34454@a#cars-34455@a#cars-35097@a#cars-35272@b#er-1708@a#er-1725@a#er-1778@b#erm-796@d#f8nrp-1183@b#jobs-3482@a#jobs-3717@c#jobs-3722@a#jobs-3728@b#jobs-3837@c#jobs-4023@b#oesx-1547@a#oesx-1803@b#oeu2u-2323@b',
        'laquesisff': 'a2b-000#aut-388#aut-716#buy-2279#buy-2489#buy-2811#dat-2874#decision-256#do-2963#euonb-114#euonb-48#grw-124#kuna-307#kuna-314#kuna-554#kuna-603#mart-555#mou-1052#oesx-1437#oesx-1643#oesx-645#oesx-867#olxeu-0000#olxeu-29763#psm-308#psm-402#psm-457#sd-570#srt-1289#srt-1346#srt-1434#srt-1593#srt-1758#srt-474#srt-475#srt-683#srt-899',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2022-09-08%2013%3A49%3A38%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.pl%2Fd%2Foferta%2Fdrewno-kominkowe-i-opalowe-dab-debowe-CID628-IDNjGjB.html%3Freason%3Dextended_search_no_results_distance%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.pl%2Fd%2Fwilkasy%2Fq-drewno-kominkowe%2F',
        'sbjs_first_add': 'fd%3D2022-09-08%2013%3A49%3A38%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.olx.pl%2Fd%2Foferta%2Fdrewno-kominkowe-i-opalowe-dab-debowe-CID628-IDNjGjB.html%3Freason%3Dextended_search_no_results_distance%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.olx.pl%2Fd%2Fwilkasy%2Fq-drewno-kominkowe%2F',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
        'PHPSESSID': '3d7puq2od3u73uo8jfvjttnp63',
        'dfp_segment': '%5B%5D',
        'sbjs_udata': 'vst%3D2%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36',
        'OptanonConsent': 'isGpcEnabled=1&datestamp=Thu+Sep+08+2022+14%3A36%3A51+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.19.0&isIABGlobal=false&hosts=&genVendors=V9%3A0%2C&consentId=027abf1f-2ede-4118-ad0a-8389d3fe9f49&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2Cgad%3A1%2CSTACK42%3A1&geolocation=PL%3B14&AwaitingReconsent=false',
        'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.olx.pl%2Fd%2Foferta%2Fdrewno-kominkowe-i-opalowe-dab-debowe-CID628-IDNjGjB.html%3Freason%3Dextended_search_no_results_distance',
        'newrelic_cdn_name': 'CF',
        '_hjIncludedInSessionSample': '0',
        '_hjSession_1685071': 'eyJpZCI6Ijk1Y2RkYmU1LWNmZDgtNGI3My05ODcwLTBkMThhYTc2Njc2MyIsImNyZWF0ZWQiOjE2NjI2NDA2MTIxMzQsImluU2FtcGxlIjpmYWxzZX0=',
        '_hjAbsoluteSessionInProgress': '0',
        'lqstatus': '1662641625|1831d1a639bx2f4419c7|er-1778||',
        '_gat_clientNinja': '1',
        '_ga': 'GA1.1.50322128.1662624083',
        'cto_bundle': 'zs-6kV9kVnpZbzkzTWoyZ3I0amlDRTBVcTlwUjl5UkRDN0JjaXA4JTJCd0ZrYThnJTJCSjY0am9nNkp2R2tTY2JMd3VrVmZHNTByanBwZDg2emxxUHFPciUyQjNOUnpRQTRocXhvYmJ3NGUlMkJiY3BKJTJCWnF2RTJUQm1YeThLc3hNVm81NzVvNHNHJTJGRVpvd2NwMDlMQnFVQyUyQkpiWUhsQmNla2M0SjFrRDUlMkJRN2x1dFdnVjN0SXhGUzdqcmxmMlZqUW5ZU2ozQTgyOFVv',
        '_ga_V1KE40XCLR': 'GS1.1.1662640610.5.1.1662640628.42.0.0',
        'session_start_date': '1662642428967',
        'onap': '1831c1e2612x28085b4c-3-1831d1a639bx2f4419c7-7-1662642429',
    }

    headers = {
        'authority': 'www.olx.pl',
        'accept': '*/*',
        'accept-language': 'pl',
        'authorization': f'Bearer {access_token}',
        'friction-token': exchange.get("token"),
        'referer': 'https://www.olx.pl/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-client': 'DESKTOP',
        'x-device-id': '71a523b6-0423-4660-9dc2-432dd10fd918',
        'x-platform-type': 'mobile-html5',
    }

    response = requests.get(f'https://www.olx.pl/api/v1/offers/{offer_id}/limited-phones/', cookies=cookies,
                            headers=headers)
    return response.json()

###############################

def get_phone_from_offer(user_id, offer_id, access_token):
    challenge = generate_challenge(user_id)
    exchange = generate_exchange(challenge)
    phone_data = fetch_phone(exchange, offer_id, access_token)
    return phone_data

########### MAIN ROUTINE ###########
har = None
with open(sys.argv[1], "rt") as fd: har = json.load(fd)
if not har: sys.exit(1)

ACCESS_TOKEN, USER_ID, OFFER_ID, user_cookies = find_access_token(har)
data = get_phone_from_offer(USER_ID, OFFER_ID, ACCESS_TOKEN)
print(data)

