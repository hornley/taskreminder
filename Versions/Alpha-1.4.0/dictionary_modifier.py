def keyPosition(dictionary, search):
    num = 0
    for key, value in dictionary.items():
        if key == search:
            return num
        num += 1

def replaceKey(dictionary, position, newKey):
    num = 0
    updatedDictionary = {}
    for key, value in dictionary.items():
        if num == position:
            updatedDictionary.update({newKey: value})
        else:
            updatedDictionary.update({key: value})
        num += 1
    return updatedDictionary

