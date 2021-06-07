import math
import re
import time

from colorama import Fore

from app.api import Tele2Api

from config import *
from log import xprint


#xekima: modified
def input_lots(data_left, display_name, min_amount, max_multiplier,
               price_multiplier, lot_type, phone_number):
    lots_to_sell = []
    index = 1
    cfg_index = 0
    while data_left >= min_amount:

        smiles = []
        wait = 0
        position = 0

        # xekima: add auto mode
        if AUTO_MODE:
            cfg = CFG[phone_number]["gb"] if lot_type == 'data' else CFG[phone_number]["min"]

            if len(cfg) <= cfg_index:
                break

            lot_data=list()
            lot_data.append(int(cfg[cfg_index]["lot"]))
            if "price" in cfg[cfg_index]:
                lot_data.append(int(cfg[cfg_index]["price"]))
                
            if "smiles" in cfg[cfg_index]:
                smiles = cfg[cfg_index]["smiles"]


            if "wait" in cfg[cfg_index]:
                wait = int(cfg[cfg_index]["wait"])
            
            if "position" in cfg[cfg_index]:
                position = int(cfg[cfg_index]["position"])


            cfg_index+=1

            lot_str = " ".join(str(x) for x in lot_data)
            if not re.match(r'^\s*\d+\s*(\s\d+\s*)?$', lot_str):
                xprint(Fore.MAGENTA, '\tIncorrect input format: '+lot_str+'. Skipping...')
                continue

        else:

            user_input = input(Fore.WHITE + f'\t{display_name}s lot {index} >>> ')

            if user_input == '':
                break

            if not re.match(r'^\s*\d+\s*(\s\d+\s*)?$', user_input):
                xprint(Fore.MAGENTA, '\tIncorrect input format. Try again')
                continue

            clean = re.sub(r'\s+', ' ', user_input.strip())
            lot_data = list(map(int, clean.split(' ')))

        amount = lot_data[0]
        if amount < min_amount:
            xprint(Fore.RED,
                  f'\tOops: {display_name.capitalize()} lot amount must be '
                  f'> {min_amount}')
            continue
        elif amount > data_left:
            xprint(Fore.RED, f'\tOops: You only have {data_left} left')
            continue

        if len(lot_data) == 1:
            price = math.ceil(amount * price_multiplier)
        else:
            price = lot_data[1]
            if price < math.ceil(amount * price_multiplier):
                xprint(Fore.RED,
                      f'\tOops: {display_name.capitalize()} lot price must be >='
                      f' ({price_multiplier} * amount)')
                continue
            elif price > max_multiplier * amount:
                xprint(Fore.RED,
                      f'\tOops: {display_name.capitalize()} lot price must be <='
                      f' ({max_multiplier} * amount)')
                continue

        xprint(Fore.GREEN,
              f'\t\tOk! Lot {index}: {amount} {display_name[:3]}.'
              f' for {price} rub.')
        data_left -= amount
        xprint('', f'\t\t({data_left} {display_name[:3]}. left)')
        lots_to_sell.append({
            'name': display_name[:3],
            'lot_type': lot_type,
            'amount': amount,
            'price': price,
            'smiles': smiles
            'position': position,
            'wait': wait
        })

        index += 1
    return lots_to_sell


async def prepare_lots(rests,phone_number):
    lots_to_sell = []

    if rests['voice'] >= 50:
        print(Fore.YELLOW + '1. Prepare minute lots:')
        lots_to_sell += input_lots(data_left=rests['voice'],
                                   display_name='minute',
                                   min_amount=50,
                                   max_multiplier=2,
                                   price_multiplier=0.8,
                                   lot_type='voice',
                                   phone_number=phone_number
                                   )
    if rests['data'] >= 1:
        print(Fore.GREEN + '2. Prepare gigabyte lots:')
        lots_to_sell += input_lots(data_left=rests['data'],
                                   display_name='gigabyte',
                                   min_amount=1,
                                   max_multiplier=50,
                                   price_multiplier=15,
                                   lot_type='data',
                                   phone_number=phone_number
                                   )
    return lots_to_sell


def print_prepared_lots(prepared_lots):
    count = len(prepared_lots)
    if count:
        xprint(Fore.LIGHTMAGENTA_EX,
              f'Ok. You have prepared {count} lot{"s" if count > 1 else ""}:')
        for lot in prepared_lots:
            color = Fore.YELLOW if lot['lot_type'] == 'voice' else Fore.GREEN

            smiles = "(" + ", ".join(lot["smiles"]) + ")" if "smiles" in lot else ""

            xprint(color, f'\t{lot["amount"]} {lot["name"]} '
                          f'for {lot["price"]} rub '+smiles)


def prepare_old_lots(old_lots: list):
    lots = []
    for lot in old_lots:
        lots.append({
            'lot_type': lot['trafficType'],
            'amount': lot['volume']['value'],
            'price': lot['cost']['amount'],
        })
    return lots


def get_if_status_is_ok(response):
    return True if response['meta']['status'] == 'OK' else False


def print_lot_listing_status(response):
    if get_if_status_is_ok(response):
        color = Fore.YELLOW if response['data']['trafficType'] == 'voice' \
            else Fore.GREEN
        amount = response['data']['volume']['value']
        uom = response['data']['volume']['uom']
        cost = response['data']['cost']['amount']
        xprint(color,
              f'Successful listing {amount} {uom} for {cost} rub.')
    else:
        xprint(Fore.RED,
              f'Error during listing... Trying Again')


async def try_sell_infinite_times(api: Tele2Api, lot: any):
    while True:
        response = await api.sell_lot(lot)
        status_is_ok = get_if_status_is_ok(response)
        print_lot_listing_status(response)
        if status_is_ok:
            '''
            {'meta': {'status': 'OK', 'message': None}, 
            'data': {'id': '-5519094492788093579', 
            'seller': {'name': '', 'emojis': []}, 
            'trafficType': 'voice', 
            'volume': {'value': 50, 'uom': 'min'}, 
            'cost': {'amount': 40.0, 'currency': 'rub'}, 
            'commission': {'amount': 0.0, 'currency': 'rub'}, 
            'status': 'active', 
            'creationDate': '2021-03-26T22:47:23.226+03:00', 
            'expirationDate': '2021-04-22T00:00:00+03:00', 
            'statusChangeDate': '2021-03-26T22:47:23.226+03:00', 
            'my': True, 
            'hash': '6078503369446081043'}}
            '''
            smiles = await api.apply_emojes(response['data']['id'], lot['price'], lot['smiles'])
            xprint(Fore.YELLOW, "Smiles added: "+"(" + ", ".join(smiles) + ")")
            if lot['position'] or lot['wait']:
                await try_resell(api, lot, response)

            break
        else:
            time.sleep(3)
            continue


async def sell_prepared_lots(api: Tele2Api, lots: list):
    for lot in lots:
        await try_sell_infinite_times(api, lot)


async def try_resell(api, lot, response):
    if lot['wait']:
        time.sleep(lot['wait'])
    
    active_lots = await api.get_active_lots()