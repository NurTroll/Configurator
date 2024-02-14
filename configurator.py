import csv
from typing import TextIO

MODELS = {
    "1": "ELTEX_2308P",
    "2": "SNR_S2982G_24TE",
    "3": "QSW2800_28T",
    "4": "QSW3500_10T",
    "5": "QSW2850_28T",
    "6": "MES2408CP",
    "7": "MES2408CP-LIFT",
    "8": "MES2428",
    "9": "MES2424"
}


# Функция создание дескрипшенов к PPPoE вланам, в зависимоти от модели записи требуются разные
def pppoe_vlans(start, finish):
    vlans = ''
    if model == 'ELTEX_2308P':
        while start <= finish:
            vlans = vlans + f'interface vlan {start}\n name PPPOE{start}\n!\n'
            start += 1
    else:
        while start <= finish:
            vlans = vlans + f'vlan {start}\n name PPPOE{start}\n!\n'
            start += 1
    return vlans.strip()


# Функция создание дескрипшенов к IPOE вланам, в зависимоти от модели записи требуются разные
def ipoe_vlans(start, finish):
    vlans = ''
    if model == 'ELTEX_2308P':
        while start <= finish:
            vlans = vlans + f'interface vlan {start}\n name IPOE{start}\n!\n'
            start += 1
    else:
        while start <= finish:
            vlans = vlans + f'vlan {start}\n name IPOE{start}\n!\n'
            start += 1
    return vlans.strip()


# Фунцкция выбора модели коммутатора для создания конфигураций
def model_found():
    while True:
        model = input("Введите номер модели коммутатора из списка:")
        for key in MODELS:
            if model == key:
                return MODELS[key]
        print('Вы ввели неверные данные, попробуйте ещё раз')


# Выводим список доступных моделей коммутаторов
for key in MODELS:
    print(f'{key} - {MODELS[key]}')
model = model_found()
# Загружаем таблицу с данными по кольцам
ips_list = list()
with open('config.csv', newline="", encoding='utf-8') as csvfile:
    config_csv = csv.reader(csvfile, delimiter=";")
    config_list = list(config_csv)
# Удаляем заголовок из таблицы и начинаем создание файлов согласно данным в ней.
header = config_list.pop(0)
files_count = 0
for config in config_list:
    if config[0] != '':
        file_input: TextIO = open('empty_configs/' + model + '.txt', "r", encoding='utf-8')
        conf_text = file_input.read()
        new_text = conf_text.replace('<managament>', config[1])
        new_text = new_text.replace('<iptv>', config[2])
        new_text = new_text.replace('<voip>', config[3])
        new_text = new_text.replace('<pppoe_start>', config[4])
        new_text = new_text.replace('<pppoe_finish>', config[5])
        new_text = new_text.replace('<ipoe_start>', config[6])
        new_text = new_text.replace('<ipoe_finish>', config[7])
        new_text = new_text.replace('<pppoe_vlans>', pppoe_vlans(int(config[4]), int(config[5])))
        new_text = new_text.replace('<ipoe_vlans>', ipoe_vlans(int(config[6]), int(config[7])))
        output = open(model + "/config" + config[0] + '.txt', 'w', encoding='utf-8')
        print(new_text, file=output)
        file_input.close()
        output.close()
        files_count += 1
# Выводим количество созданных файлов, должно быть 48 как и колец.
print('Создано файлов: {}'.format(files_count))
