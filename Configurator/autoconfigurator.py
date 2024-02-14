import csv
from typing import TextIO

MASK = {
    "24": "255.255.255.0",
    "25": "255.255.255.128",
    "26": "255.255.255.192",
    "27": "255.255.255.224",
    "28": "255.255.255.240",
    "29": "255.255.255.248",
    "30": "255.255.255.252"
}

# MODELS = {
#     "1": "ELTEX_2308P",
#     "2": "SNR_S2982G_24TE",
#     "3": "QTech_QSW2850_28T",
#     "4": "QSW3500_10T",
#     # "5": "QTech_QSW3750_28T",
#     # "6": "QTech_QSW3470_28T",
#     # "7": "QTech_QSW4610_28T",
#     # "8": "Eltex_MES2428",
#     # "9": "Eltex_MES2408"
# }

VENDORS = {"ELTEX": {"ELTEX_2308P", "MES2428", "MES2408CP", "MES2408CP-LIFT", "MES2424"},
           "Qtech": {"QSW2850_28T", "QSW2800_28T", "QSW3750_28T",
                 "QSW3470_28T", "QSW4610_28T", "QSW3500_10T"},
           "SNR": {"SNR_S2982G_24TE", "SNR_S2985G_24TE"}
           }


# Функция вычисления шлюза
def gw_define(ip, mask):
    ip2 = int(ip.split('.')[3])
    mask2 = int(mask.split('.')[3])
    gw = ip.rpartition('.')[0] + '.' + str((ip2 & mask2) + 1)
    return gw


def model_found():
    while True:
        model = input("Введите номер модели коммутатора из списка:").strip()
        for key in MODELS:
            if model == key:
                return MODELS[key]
        print('Вы ввели неверные данные, попробуйте ещё раз')


def mask_found():
    while True:
        mask1 = input("Введите маску подсети:").strip()
        for key in MASK:
            if mask1 == key:
                return MASK[key]
        print('Вы ввели неверные данные, попробуйте ещё раз')


# Проверка верности вводимых данных номера кольца
def ring_input():
    while True:
        ring = input("Введите номер кольца от 1 до 48(49 для нестандартных конфигураций):").strip()
        if ring.isdigit() and (int(ring) >= 0) and (int(ring) < 50):
            return ring
        print('Вы ввели неверные данные, попробуйте ещё раз')


# Проверка верности вводимых данных ip адреса
def ip_input():
    while True:
        ip = input("Введите ip:").strip()
        ip_split = ip.split('.')
        if (ip.count('.') == 3 and ip_split[0].isdigit() and ip_split[1].isdigit() and ip_split[2].isdigit() and
            len(ip_split[0]) < 4 and len(ip_split[1]) < 4 and len(ip_split[3]) < 4 ) :
            return ip
        print('Вы ввели неверные данные, попробуйте ещё раз')


def get_pppoe_range(ring):
    with open('config.csv', newline="", encoding='utf-8') as csvfile:
        config_csv = csv.reader(csvfile, delimiter=";")
        config_list = list(config_csv)
    # Удаляем заголовок из таблицы и начинаем создание файлов согласно данным в ней.
    header = config_list.pop(0)
    for ring_number in config_list:
        if ring_number[0] == ring:
            return ring_number[4], ring_number[5]


def pppoe_main_check(range):
    while True:
        main_vlan = input(f'Ввведите номер мейн влана из диапозона {range[0]} - {range[1]}: ')
        if main_vlan == '':
            return range[0]
        elif main_vlan.isdigit() and range[0] <= main_vlan <= range[1]:
            return main_vlan
    print('Вы ввели неверные данные, попробуйте ещё раз')

'''
print("1 - ELTEX\n2 - QTECH\n3 - SNR")
vendor_number = input("Введите номер соответствующий производителю:")
MODELS = VENDORS.get(vendor_number)
for key in MODELS:
    print(f'{key} - {MODELS[key]}')
model = model_found()
ring = ring_input()
main = pppoe_main_check(get_pppoe_range(ring))
hostname = input('Введите имя коммутатора:').strip()
ip = ip_input()
for key in MASK:
    print(f'/{key} - {MASK[key]}')
mask = mask_found()
gw = gw_define(ip, mask)
print(f'{hostname} {ip} {mask} {gw}')
config_ring = open(model + '/config' + ring + '.txt', 'r', encoding='utf-8')
conf_text = config_ring.read()
new_text = conf_text.replace('<hostname>', hostname)
new_text = new_text.replace('<ip>', ip)
new_text = new_text.replace('<mask>', mask)
new_text = new_text.replace('<gw>', gw)
new_text = new_text.replace('PPPOE' + main, 'PPPOE-MAIN')
filename = hostname + '.conf'
output = open('backup/' + filename, 'w', encoding='utf-8')
output2 = open("/mnt/disk_e/tftp/startup.conf", 'w', encoding='utf-8')
print(new_text, file=output)
print(new_text, file=output2)
config_ring.close()
output.close()
output2.close()
'''
