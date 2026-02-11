def interpret_pss10():
    distress_ids = [1, 2, 3, 6, 9 ,10]
    cooping_ids = [4, 5, 7, 8]

    distress = sum(answers[q] for q in distress_ids)
    cooping = sum([4 - answers[q]] if answers[q] in [0,1,3,4] else answers[q] for q in cooping_ids)
    total = distress + cooping

    if total <= 13:
        return 'Низкий уровень стресса'
    elif total <= 26:
        return 'Средний уровень стресса'
    else:
        return 'Высокий уровень стресса'

def interpret_gad7():
    total = distress + cooping

    if total <= 13:
        return 'Легкий уровень тревоги'
    elif total <= 26:
        return 'Умеренный уровень тревоги'
    else:
        return 'Высокий уровень тревоги'

def interpret_phq15():
    total = distress + cooping

    if total <= 4:
        return 'Минимальный уровень соматической нагрузки'
    elif total <= 9:
        return 'Низкий уровень соматической нагрузки'
    elif total <= 14:
        return 'Умеренный уровень соматической нагрузки'
    else:
        return 'Высокий уровень соматической нагрузки'

def interpret_mbi():
    total = distress + cooping

    if total <= 4:
        return 'Минимальный уровень соматической нагрузки'
    elif total <= 9:
        return 'Низкий уровень соматической нагрузки'
    elif total <= 14:
        return 'Умеренный уровень соматической нагрузки'
    else:
        return 'Высокий уровень соматической нагрузки'

def interpret_hads():
    total = distress + cooping

    if total <= 4:
        return 'Минимальный уровень соматической нагрузки'
    elif total <= 9:
        return 'Низкий уровень соматической нагрузки'
    elif total <= 14:
        return 'Умеренный уровень соматической нагрузки'
    else:
        return 'Высокий уровень соматической нагрузки'
