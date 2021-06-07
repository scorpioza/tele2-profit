# Автоматический режим. Если False, скрипт выдает меню пользователя
AUTO_MODE=True

# Только для продажи в ручном режиме! (AUTO_MODE=False)
# В случае True в начале работы скрипта выставленные лоты удаляются
DELETE_ACTIVE_LOTS=False

# сохранение сообщений в лог
PRINT_TO_LOG = True

# относительный или абсолютный
LOG_PATH = "tele.log"

# путь к конфигу
CONFIG_PATH = "tele2-profit/config-{phone_number}.json"

# названия смайлов из api tele2
SMILES = ["bomb", "cat", "cool", "devil", "rich", "scream", "tongue", "zipped"]

# -----------------------------------------------------------------

# Пример лота (GB или MIN)
#{"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10}

CFG = {
    "79777660388": {
        "gb": [
            {"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10},
            #{"lot": 2, "price": 31}
        ],
        "min": [
            {"lot": 50, "price": 42, "smiles": ["bomb", "cat", "bomb"], "wait": 5, "position": 10},
            #{"lot": 90, "price": 72}
        ]
    },
    "79016974663": {
        "gb": [
            {"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"], "wait": 5, "position": 10},
            # {"lot": 2, "price": 31}
        ],
        "min": [
            {"lot": 50, "price": 42, "smiles": ["bomb", "cat", "bomb"], "wait": 5, "position": 10},
            # {"lot": 90, "price": 72}
        ]
    }
}
