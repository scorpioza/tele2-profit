from colorama import Fore

from app.api import Tele2Api

from log import xprint



async def print_balance(api):
    balance = await api.get_balance()
    xprint(Fore.YELLOW,  'Balance: ')
    xprint(Fore.MAGENTA, f'{balance} rub.', True)


async def print_rests(api: Tele2Api):
    print('Checking your rests...')
    print(
        Fore.CYAN + 'note: only plan (not market-bought ones nor transferred)'
                    ' rests can be sold')
    rests = await api.get_rests()
    xprint(Fore.WHITE,  'You have')
    xprint(Fore.YELLOW, f'\t{rests["voice"]} min')
    xprint(Fore.GREEN, f'\t{rests["data"]} gb')
    xprint(Fore.WHITE, '\t\tavailable to sell.')
    return rests
