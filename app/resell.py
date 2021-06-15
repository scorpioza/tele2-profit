
import time
from colorama import Fore
from app.api import Tele2Api
from config import *
from log import xprint
import random
import requests
import json



REQUEST_HEADERS = {'User-agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.151 Safari/537.36'}

OFFSET_LOTS=0

REGIONS = [
        "https://msk.tele2.ru/",
        "https://spb.tele2.ru/",
        "https://chelyabinsk.tele2.ru/",
        "https://rostov.tele2.ru/",
        "https://irkutsk.tele2.ru/",
        "https://ekt.tele2.ru/",
        "https://nnov.tele2.ru/",
        "https://barnaul.tele2.ru/",
        "https://arh.tele2.ru/",
        "https://belgorod.tele2.ru/",
        "https://bryansk.tele2.ru/",
        "https://vladimir.tele2.ru/",
        "https://volgograd.tele2.ru/",
        "https://vologda.tele2.ru/",
        "https://voronezh.tele2.ru/",
        "https://eao.tele2.ru/",
        "https://ivanovo.tele2.ru/",
        "https://irkutsk.tele2.ru/",
        "https://kaliningrad.tele2.ru/",
        "https://kaluga.tele2.ru/",
        "https://kamchatka.tele2.ru/",
        "https://kuzbass.tele2.ru/",
        "https://kirov.tele2.ru/",
        "https://kostroma.tele2.ru/",
        "https://krasnodar.tele2.ru/",
        "https://krasnoyarsk.tele2.ru/",
        "https://norilsk.tele2.ru/",
        "https://kurgan.tele2.ru/",
        "https://kursk.tele2.ru/",
        "https://lipetsk.tele2.ru/",
        "https://magadan.tele2.ru/",
        "https://msk.tele2.ru/",
        "https://murmansk.tele2.ru/",
        "https://nnov.tele2.ru/",
        "https://novgorod.tele2.ru/",
        "https://novosibirsk.tele2.ru/",
        "https://omsk.tele2.ru/",
        "https://orenburg.tele2.ru/",
        "https://orel.tele2.ru/",
        "https://penza.tele2.ru/",
        "https://perm.tele2.ru/",
        "https://vladivostok.tele2.ru/",
        "https://pskov.tele2.ru/",
        "https://altai.tele2.ru/",
        "https://buryatia.tele2.ru/",
        "https://karelia.tele2.ru/",
        "https://komi.tele2.ru/",
        "https://mariel.tele2.ru/",
        "https://mordovia.tele2.ru/",
        "https://kazan.tele2.ru/",
        "https://khakasia.tele2.ru/",
        "https://rostov.tele2.ru/",
        "https://ryazan.tele2.ru/",
        "https://samara.tele2.ru/",
        "https://spb.tele2.ru/",
        "https://saratov.tele2.ru/",
        "https://sakhalin.tele2.ru/",
        "https://ekt.tele2.ru/",
        "https://smolensk.tele2.ru/",
        "https://tambov.tele2.ru/",
        "https://tver.tele2.ru/",
        "https://tomsk.tele2.ru/",
        "https://tula.tele2.ru/",
        "https://tyumen.tele2.ru/",
        "https://izhevsk.tele2.ru/",
        "https://uln.tele2.ru/",
        "https://hmao.tele2.ru/",
        "https://chelyabinsk.tele2.ru/",
        "https://chuvashia.tele2.ru/",
        "https://yanao.tele2.ru/",
        "https://yar.tele2.ru/"]

REQ = "api/exchange/lots?trafficType={type}&volume={volume}&cost={cost}&offset={offset}&limit={limit}"


def getData(response, limit):

    amount = response['data']['volume']['value']
    uom = response['data']['volume']['uom']
    price = int(response['data']['cost']['amount'])

    lot_type = "voice" if uom=="min" else "data"

    r = random.choice(REGIONS)
    r += REQ.format(type=lot_type, volume=str(amount), cost=str(price),
                    offset=str(OFFSET_LOTS), limit=str(limit))

    x = requests.get(r, headers=REQUEST_HEADERS)
    if x.status_code != 200:
        xprint(Fore.YELLOW, "ERROR: " + str(x.status_code) + x.text)
        return
    info = json.loads(x.text)
    if info["meta"]["status"] != "OK":
        xprint(Fore.YELLOW, "ERROR: " + str(x.text))
        return

    '''
    info["data"]
    [{'id': '690892699412458274', 'seller': {'name': 'Руслан', 'emojis': []}, 'trafficType': 'data', 'volume': {'value': 1, 'uom': 'gb'}, 'cost': {'amount': 16.0, 'currency': 'rub'}, 'commission': {'amount': 0.0, 'currency': 'rub'}, 'status': 'active', 'my': False, 'hash': '-5620704130575470244'}, {'id': '2241801704193553322', 'seller': {'name': None, 'emojis': []}, 'trafficType': 'data', 'volume': {'value': 1, 'uom': 'gb'}, 'cost': {'amount': 16.0, 'currency': 'rub'}, 'commission': {'amount': 0.0, 'currency': 'rub'}, 'status': 'active', 'my': False, 'hash': '-5539719007466376523'}]

    '''

    return info["data"]


async def try_resell(params):

    # 'volume': {'value': 50, 'uom': 'min'}, 
    # 'cost': {'amount': 40.0, 'currency': 'rub'}, 
    curlot = params['lot']
    response = params["response"]
    wait= params["wait"]

    amount = str(response['data']['volume']['value'])
    uom = str(response['data']['volume']['uom'])
    price = int(response['data']['cost']['amount'])
    new_price = int(curlot['price'])+1

    if wait and 'wait' in curlot and curlot['wait']:
        time.sleep(curlot['wait'])

    async with Tele2Api(params['phone_number'], params['access_token'], params['refresh_token']) as api:

        if 'position' in curlot and curlot['position']:
            lots_in_list = getData(response, curlot['position'])
            #print("======= LOTS IN LIST ============")
            #print(lots_in_list)
            #print("======= /LOTS IN LIST ============")

            wait_next=False
            if lots_in_list:
                for lot in lots_in_list:
                    if lot["id"]==response['data']['id']:
                        wait_next=True
                        break
            else:
                wait_next=True

            if not wait_next:
                await api.change_price(response['data']['id'], curlot['price']+1)
                xprint(Fore.YELLOW, "Set price "+str(new_price)+" for lot "+amount+" ("+uom+")")
            else:
                time.sleep(WAIT_FOR_NEXT_CHECK_LOT_POS)
                xprint(Fore.YELLOW, "WAITING for change price "+str(new_price)+" for lot "+amount+" ("+uom+")")
                
                params['wait']=False
                await try_resell(params)
        else:
            await api.change_price(response['data']['id'], curlot['price']+1)
            xprint(Fore.YELLOW, "Set price "+str(new_price)+" for lot "+amount+" ("+uom+")")
