# Автоматический режим. Если False, скрипт выдает меню пользователя
AUTO_MODE=True

# Только для продажи в ручном режиме! (AUTO_MODE=False)
# В случае True в начале работы скрипта выставленные лоты удаляются
DELETE_ACTIVE_LOTS=False

# сохранение сообщений в лог
PRINT_TO_LOG = True

# относительный или абсолютный
LOG_PATH = "tele.log"

# названия смайлов из api tele2
SMILES = ["bomb", "cat", "cool", "devil", "rich", "scream", "tongue", "zipped"]

# -----------------------------------------------------------------

# Пример лота (GB или MIN)
#{"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"]}

CFG_GB = [
    #{"lot": 1, "price": 16, "smiles": ["bomb", "cat", "cool"]},
    #{"lot": 2, "price": 31}
]

CFG_MIN = [
    {"lot": 50, "price": 42, "smiles": ["bomb", "cat", "bomb"]},
    #{"lot": 90, "price": 72}
]
