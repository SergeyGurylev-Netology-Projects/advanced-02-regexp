import re
import csv

contacts_list = []
pattern_fio = re.compile(r"(\w+)\s?(\w+)?\s?(\w+)?")
pattern_phone = re.compile(r"(\+7|\b8)[\s\(-]*(\d*)[\)\s-]*(\d*)[\s-]*(\d*)[\s-]*(\d*)\s*\(?(доб\.?\s*\d*)?\)?")


def repl_phone(m):
    ss = ''
    for i in range(1,max(m.lastindex,5)):
        ss += m.group(i+1)
    ss = f'+7({ss[0:3]}){ss[3:6]}-{ss[6:8]}-{ss[8:10]}'
    if m.lastindex==6:
        ss += ' '+m.group(6)
    return ss


with open("phonebook_raw.csv", encoding='utf-8') as f:
    line = f.readline().strip()
    contacts_list.append(line.split(','))
    while True:
        line = f.readline().strip()
        if line == '':
            break

        data = line.split(',')

        phone = pattern_phone.sub(repl_phone, data[5])

        # Вариант 1
        # fio = re.split(r'\W+', f"{data[0]} {data[1]} {data[2]}")
        # Вариант 2
        # fio = re.sub(pattern_fio, r"\1 \2 \3", f"{data[0]} {data[1]} {data[2]}").split(' ')
        # Вариант 3. Все три варианта рабочие
        fio = [
            re.sub(pattern_fio, r"\1", f"{data[0]} {data[1]} {data[2]}").strip(),
            re.sub(pattern_fio, r"\2", f"{data[0]} {data[1]} {data[2]}").strip(),
            re.sub(pattern_fio, r"\3", f"{data[0]} {data[1]} {data[2]}").strip()
        ]

        filter_index = next((i for i, x in enumerate(contacts_list)
                             if x[0] == fio[0] and x[1] == fio[1]), None)
        if filter_index is None:
            new_line = [fio[0], fio[1], fio[2], data[3], data[4], phone, data[6]]
            contacts_list.append(new_line)
        else:
            new_line = contacts_list[filter_index]
            for id in range(3,7):
                if new_line[id]=='':
                    new_line[id] = data[id]

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list)
