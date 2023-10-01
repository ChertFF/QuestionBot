import logging
import os
from time import strftime, gmtime

# Получаем текущий путь к скрипту
current_path = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к папке с логами
logs_folder = os.path.join(current_path, 'out')

# Создаем папку, если она не существует
os.makedirs(logs_folder, exist_ok=True)

# Формируем имя файла логов
time = strftime("%m.%d.%Y_%H.%M.%S", gmtime())
filename_path = os.path.join(logs_folder, f'logs_{time}.log')
print(filename_path)

# Настройка логгера
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO, filename=filename_path)
