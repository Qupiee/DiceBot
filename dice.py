import random

# range of 2 and 12. because min summ will be 2
help_message = "Выберите диапазон от 2 до 12 из трех чисел включительно. Сделайте ставку. "\
    "Если выпадает пара чисел, сумма которых входит в выбранный вами диапазон, вы получаете двойной выигрыш от вашей ставки. Иначе теряете поставленную сумму.\n\n" \
    "Например, диапазон от 6 до 8 и ставка 300. Вы выиграете 600, если сумма, выпавшей пары чисел будет равна: 6, 7, 8. Иначе теряете 300."

# game line
bet = 0
balance = 1000
bet_line = 'Сделайте ставку'
balance_line = 'Ваш баланс: '
get_less_line = 'Выберите перове число из диапазона'
get_more_line = 'Выберите второе число из диапазона'

# exceptions
error = 'Что-то не так'
not_enough = 'На вашем счету нет такой суммы'

# game result
win_message = '. Вы выиграли'
lose_message = '. Вы проиграли'
result = 'tomato'
differ = 0


def dice_roll(range_less, range_more):
    global result  # let 'bot.py' use var 'result'
    global differ
    result = 'tomato'
    differ = 0
    first_num = random.randint(1, 6)
    second_num = random.randint(1, 6)
    summ = 0
    summ = first_num + second_num
    differ = range_more - range_less
    if range_less >= range_more or differ >= 3 or differ < 0 or range_less < 2 or summ < 2:  # more is more not less. limit of range, up to 3 nums. min num = 1
        range_less = 0
        range_more = 0
        return error
    # исправить условия выигрыша
    if range_less <= summ <= range_more and range_less < range_more:
        if bet <= balance:  # check for correct balance
            result = 'win'
            return 'Выпало ' + str(summ) + win_message
        else:
            return not_enough
    # исправить условия проигрыша
    elif range_less < range_more:
        if bet <= balance:
            result = 'lose'
            return 'Выпало ' + str(summ) + lose_message
        else:
            return not_enough
