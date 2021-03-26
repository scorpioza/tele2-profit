from colorama import init as colorama_init, Fore

from app.account import print_balance
from app.api import Tele2Api
from app.auth import input_phone_number, write_config_to_file, get_tokens
from app.utils import run_main
from app.menu import display_menu, menu_new_action, menu_again_action
from app.startup import delete_active_lots, try_load_config
from app.timer import activate_timer_if_needed

from config import *
from log import xprint


async def login_pipeline(phone_number: str):
    async with Tele2Api(phone_number) as api:
        access_token, refresh_token = await get_tokens(api, phone_number)
        xprint(Fore.GREEN, 'Successful auth!')
        write_config_to_file(phone_number, access_token, refresh_token)
        xprint(Fore.YELLOW, 'Auth data saved to ' + Fore.BLUE + 'config.json')
        return access_token, refresh_token


async def try_refresh_tokens_or_get_new(api: Tele2Api, phone_number: str,
                                        refresh_token: str):
    try:
        access_token, refresh_token = await api.refresh_tokens(refresh_token)
        return access_token, refresh_token
    except TypeError:
        xprint(Fore.RED, 'Your auth expired. Sending new SMS to ')
        xprint(Fore.GREEN, phone_number)
        access_token, refresh_token = await login_pipeline(phone_number)
        return access_token, refresh_token


async def authenticate(phone_number: str, access_token: str,
                       refresh_token: str):
    async with Tele2Api(phone_number, access_token, refresh_token) as api:
        is_authorized = await api.check_if_authorized()
        if not is_authorized:
            access_token, refresh_token = await try_refresh_tokens_or_get_new(
                api,
                phone_number,
                refresh_token)
            write_config_to_file(phone_number, access_token, refresh_token)
            await authenticate(phone_number, access_token, refresh_token)
        return access_token, refresh_token


async def main_pipeline(phone_number: str, access_token: str,
                        refresh_token: str):
    async with Tele2Api(phone_number, access_token, refresh_token) as api:
        await print_balance(api)
        if DELETE_ACTIVE_LOTS:
            deleted_lots = await delete_active_lots(api)
        else:
            deleted_lots = []
        xprint(Fore.MAGENTA, '-----')
        option = await display_menu(display_again_action=len(deleted_lots) > 0)
        if option == 'new':
            await menu_new_action(api)
        elif option == 'again':
            await menu_again_action(api, deleted_lots)
        elif option == 'Exit':
            return
        await activate_timer_if_needed(api)

# xekima - add auto mode 
async def main_auto_mode(phone_number: str, access_token: str,
                        refresh_token: str):
    async with Tele2Api(phone_number, access_token, refresh_token) as api:
        await print_balance(api)
        await menu_new_action(api)

async def main():
    colorama_init(True)

    config = try_load_config()

    if not config:
        phone_number = input_phone_number()
        access_token, refresh_token = await login_pipeline(phone_number)
    else:
        phone_number, access_token, refresh_token = config

    access_token, refresh_token = await authenticate(phone_number, access_token,
                                                     refresh_token)
    #xekima: mode switcher
    if AUTO_MODE:                                                 
        await main_auto_mode(phone_number, access_token, refresh_token)
    else: 
        await main_pipeline(phone_number, access_token, refresh_token)

if __name__ == '__main__':
    run_main(main)
