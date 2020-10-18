import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import re


def extract_items():
    driver = webdriver.Chrome()
    driver.get("https://groceries.asda.com")
    elem = driver.find_element_by_class_name('navigation-menu')
    elem = elem.find_element_by_tag_name('button')
    elem.click()

    all_lists = driver.find_element_by_class_name('h-nav')
    all_lists = all_lists.find_elements_by_tag_name('ul')
    categories = all_lists[0].find_elements_by_tag_name('li')

    all_items = []

    for c in categories:
        hover = ActionChains(driver).move_to_element(c)
        hover.perform()
        all_lists = driver.find_element_by_class_name('h-nav')
        all_lists = all_lists.find_elements_by_tag_name('ul')

        small_categories = all_lists[1].find_elements_by_tag_name('li')
        for s in small_categories:
            hover = ActionChains(driver).move_to_element(s)
            hover.perform()
            all_lists = driver.find_element_by_class_name('h-nav')
            all_lists = all_lists.find_elements_by_tag_name('ul')

            if len(all_lists) > 2:
                items = all_lists[2].find_elements_by_tag_name('li')

                for i in items:
                    hover = ActionChains(driver).move_to_element(i)
                    hover.perform()

                    all_lists = driver.find_element_by_class_name('h-nav')
                    all_lists = all_lists.find_elements_by_tag_name('ul')

                    if len(all_lists) > 3:
                        small_items = all_lists[3].find_elements_by_tag_name('li')

                        for si in small_items:
                            all_items.append(si.text)
                            print(si.text)
                    else:
                        all_items.append(i.text)
                        print(i.text)

    driver.close()

    seen = set()
    seen_add = seen.add
    all_items = [x for x in all_items if not (x in seen or seen_add(x))]

    with open('items.txt', 'w') as f:
        f.write("\n".join(all_items))


def separate_items():
    with open('items.txt', 'r') as f:
        all_items = f.read()

    all_items = all_items.replace(' & ', "\n")
    all_items = all_items.replace(', ', "\n")

    with open('items2.txt', 'w') as f:
        f.write(all_items)


def remove_unwanted():
    with open('items2.txt', 'r') as f:
        all_items = f.read()

    all_items = all_items.split('\n')
    new_items = []

    for line in all_items:
        if 'View' not in line:
            line = re.sub('[^A-Za-z0-9 ]+', '', line)
            new_items.append(line)

    seen = set()
    seen_add = seen.add
    new_items = [x for x in new_items if not (x in seen or seen_add(x))]

    new_items = '\n'.join(new_items)

    with open('items3.txt', 'w') as f:
        f.write(new_items)


def convert_to_lower(file_name = 'items3.txt'):
    with open(file_name, 'r') as f:
        all_items = f.read()

    with open(file_name, 'w') as f:
        all_items = all_items.lower()
        f.write(all_items)