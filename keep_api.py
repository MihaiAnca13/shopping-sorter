import gkeepapi
import keyring
from quick_sort import quickSort


def find_item(note, id):
    for item in note.unchecked:
        if item.id == id:
            return item


username = "mihai.anca13@gmail.com"

keep = gkeepapi.Keep()
token = keyring.get_password('google-keep-token', username)
keep.resume(username, token)

gnote = keep.get('1tKJr20yppE8-meRaUnudYpQL7X1-qszMfMdcM90f2SgDFCJFiyHCRcjLKojhEXm16P6XJA')

parents = []
for item in gnote.unchecked:
    if item.parent_item is None:
        parents.append(item.id)

for p in parents:
    parent = find_item(gnote, p)

    # Hardcoded to only sort asda's list
    if parent.text != "Asda":
        continue

    items_to_sort = []
    for item in parent.subitems:
        if not item.checked:
            items_to_sort.append(item)

    quickSort(items_to_sort, 0, len(items_to_sort) - 1)

keep.sync()
