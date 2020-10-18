import re
import collections


def get_item_value(item):
    with open('item_db.txt', 'r') as f:
        item_db = f.read().split('\n')

    pattern = ""
    for name in item.text.split(' '):
        if name != "" and len(name) > 1:
            if name[-1] == "s":
                pattern += f"({name.lower()[:-1]}[s]*)*"
            else:
                pattern += f"({name.lower()})*"

    r = re.compile(pattern)

    findings = collections.defaultdict(int)
    for idx, name in enumerate(item_db):
        m = r.finditer(name)
        for i in m:
            i_span = i.span()
            if i_span[1] - i_span[0] > 0:
                findings[idx+1] += i_span[1] - i_span[0]

    max_val = 0
    max_idx = 0
    for idx, val in findings.items():
        if val > max_val:
            max_idx, max_val = idx, val

    return max_idx


def swap_items(item1, item2):
    item1.sort, item2.sort = item2.sort, item1.sort


def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high]  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if get_item_value(arr[j]) <= get_item_value(pivot):
            # increment index of smaller element
            i = i + 1
            swap_items(arr[i], arr[j])
            arr[i], arr[j] = arr[j], arr[i]

    swap_items(arr[i + 1], arr[high])
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


def quickSort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


class Item:
    text = ""

    def __init__(self, text):
        self.text = text


if __name__ == "__main__":
    a = Item('frozen fruits 1kg')
    print(get_item_value(a))