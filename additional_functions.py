def unpacking_txt(file):
    with open(file, "r", encoding="utf8") as text:
        strings = text.readlines()
    keys = list(filter(lambda string: ":" in string or " - " in string, strings))
    data = {}
    for i in strings:
        if i in keys:
            if ":" in i:
                data[i[:-2]] = []
            elif " - " in i:
                data[i[:i.index(" - ")]] = i[i.index(" - ") + 3:].strip()
        else:
            data[list(data.keys())[-1]].append(i.strip())
    return data


def unpacking_txt_to_map(file):
    data = unpacking_txt(file)
    for i in data.keys():
        new_dict = {}
        for j in data[i]:
            new_dict[j.split("{")[0]] = tuple(map(float, j.split("{")[1][:-1].split(";")))
        data[i] = new_dict
    return data
