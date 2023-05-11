import re


def get_ordinal_number(word):
    # 判断pattern

    pattern = r'(\d+)(st|nd|rd|th)'
    match = re.search(pattern, word)
    if match:
        print(match)
        number = int(match.group(1))
        return number

    ordinals = {
        'last': -1,
        'first': 1,
        '1st': 1,
        'second': 2,
        '2nd': 2,
        'third': 3,
        '3rd': 3,
        'fourth': 4,
        '4th': 4,
        'fifth': 5,
        '5th': 5,
        'sixth': 6,
        '6th': 6,
        'seventh': 7,
        '7th': 7,
        'eighth': 8,
        '8th': 8,
        'ninth': 9,
        '9th': 9,
        'tenth': 10,
        'eleventh': 11,
        '32rd': 32
    }
    return ordinals.get(word.lower(), None)


def analyze_gpt(text):
    results = []
    data_list = text.split(' || ')
    for item in data_list:
        item_list = item.split(' (')
        results.append((item_list[0], item_list[1][:-1]))
    formatted_list = []
    for president in results:
        name, term = president
        start_date = term.strip()
        end_date = start_date  # 默认与起始时间相同
        if '-' in term:
            start_date, end_date = term.split('-')
            start_date = start_date.strip()
            end_date = end_date.strip()
            if end_date.lower() == 'present':
                end_date = '2099'
        formatted_list.append([name, start_date, end_date])
    return formatted_list
