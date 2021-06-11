from colorama import init as colorama_init, Fore
from config import *
from log import xprint
from app.startup import delete_active_lots, try_load_config, print_active_lots, update_active_lots
from app.api import Tele2Api
from app.utils import run_main
from main import login_pipeline

from app.resell import try_resell


async def changeActiveLot():
    colorama_init(True)

    phone_number = "79016974663"

    xprint(Fore.MAGENTA, '# PHONE: '+phone_number+" #")

    config = try_load_config(phone_number)

    if not config:
        #phone_number = input_phone_number()
        access_token, refresh_token = await login_pipeline(phone_number)
    else:
        phone_number, access_token, refresh_token = config

    zlot = None

    async with Tele2Api(phone_number, access_token, refresh_token) as api:
        active_lots = await api.get_active_lots()
        #print(active_lots)
        
        for lot in active_lots:
            amount = str(lot['volume']['value'])
            uom = str(lot['volume']['uom'])
            price = int(lot['cost']['amount'])
            #print("-----")
            #print(amount+" - "+uom+" - "+str(price))
            if amount == "1" and uom == "gb" and price ==17:
                zlot = lot

    if zlot:
        print(zlot["id"])
        print(zlot)

    response = {"data": zlot}
    wait = True
    curlot = {"lot": 1, "price": 17, "smiles": ["bomb", "cat", "cool"], "wait": 1, "position": 20}
    
    await try_resell(api, curlot, response, wait)

async def main():
    await changeActiveLot()

if __name__ == '__main__':
    run_main(main)
