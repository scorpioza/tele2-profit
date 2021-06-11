# Автоматический режим. Если False, скрипт выдает меню пользователя
AUTO_MODE=True

# Только для продажи в ручном режиме! (AUTO_MODE=False)
# В случае True в начале работы скрипта выставленные лоты удаляются
DELETE_ACTIVE_LOTS=False

# сохранение сообщений в лог
PRINT_TO_LOG = True

# относительный или абсолютный
LOG_PATH = "tele.log"

# путь к конфигу - ввести необходимый предварительный путь
CONFIG_PATH = "config-{phone_number}.json" #tele2-profit/

# названия смайлов из api tele2
SMILES = ["bomb", "cat", "cool", "devil", "rich", "scream", "tongue", "zipped"]

# время повторного ожидания проверки позиции лота в секундах. Вначале ожидаем время,
# указанное в параметре "wait"
WAIT_FOR_NEXT_CHECK_LOT_POS=10


# -----------------------------------------------------------------

# Пример лота (GB или MIN). wait - секунды
#{"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10}

CFG_DEFAULT = {"wait": 0, "position": 0}

CFG = {
    "79016956231": {
        "gb": [
            {"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10},
            #{"lot": 2, "price": 31}
        ],
        #"min": [
            #{"lot": 50, "price": 42, "smiles": ["bomb", "cat", "bomb"], "wait": 5, "position": 10},
            #{"lot": 90, "price": 72}
        #]
    },
    "79016974663": {
        "gb": [
            {"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10},
            # {"lot": 2, "price": 31}
        ],
        #"min": [
            #{"lot": 50, "price": 42, "smiles": ["bomb", "cat", "bomb"], "wait": 5, "position": 10},
            # {"lot": 90, "price": 72}
        #]
    }
}
