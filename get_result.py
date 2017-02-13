import json

if __name__ == '__main__':

    date_all = 0
    date_empty = 0
    date_before = 0
    date_after = 0

    all_avito_adverts = 36420

    with open('coins.json') as coins_file:
        coins = json.load(coins_file)

        date_all = len(coins)

        for coin in coins:
            if coin['date'] == None: date_empty += 1
            elif coin['date'] <= 2000: date_before += 1
            elif coin['date'] > 2000: date_after += 1

    print('Всего объявлений: ' + str(date_all))
    print('Объявлений без указания даты: ' + str(date_empty))
    print('Объявлений с монетами до 2000: ' + str(date_before))
    print('Объявлений с монетами после 2000: ' + str(date_after))

    print('\n')
    print('Дата не указана: ' + str(date_empty))
    print('До 2000 / После 2000: ' + str(date_before / date_after))

    print('\n')
    print('С умножением на коэффициент: ' + str(all_avito_adverts/date_all))
    print('Дата не указана: ' + str(date_empty*all_avito_adverts/date_all))
    print('До 2000 / После 2000: ' + str(date_before/date_after))

