from selenium import webdriver # импорт вебдрайвера
from datetime import timedelta, datetime # импорт функции дельты для работы с datatime
import time # модуль работы с временем
import re # регулярные выражения


# параметры фильтрации
days_pub = 20 # количество прошедших дней с момента публикации
acc_subcriptions = 500 # количество допустимых подписок
publications = 10 # минимум публикаций

today = datetime.now()

from selenium.common.exceptions import NoSuchElementException # исключения для отсутствия элемента
from selenium.common.exceptions import StaleElementReferenceException # исключение для устаревшего элемента

# функция существования элеммента на странице
def xpath_existence (url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence

browser = webdriver.Chrome("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\chromedriver.exe") # переменная для работы с браузером

# считывание ссылок на профили из файла massiv.txt
f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\massiv.txt", 'r')
file_list = []
for line in f:
    file_list.append(line)
f.close()

'''
Обработка ссылок:
1. аккаунт должен быть публичным;
2. число подписок аккаунта должно быть меньше значения переменной acc_subcriptions;
3. не должно быть ссылок на сайты;
4. необходимо фото профиля;
5. число публикаций аккаунта должно быть больше значения переменной publications;
6. последняя публикация должна быть не менее days_pub дней.
'''
filtered_list = []
i = 0 # количество подходящих пользователей
j = 0 # номер вывода в терминале

for follower in file_list:
    j += 1
    browser.get(follower)
    time.sleep(1.5)

    # 1. проверка на публичность аккаунта
    element = "//section/main/div/div/article/div/div/h2"
    if xpath_existence(element) == 1:
        try:
            if browser.find_element_by_xpath(element).text == "This Account is private" or "Это закрытый аккаунт":
                print(j, "Приватный аккаунт")
                continue
        except StaleElementReferenceException:
            print("Ошибка, код ошибки: 1")

    # 2. проверка на допустимое число подписок
    element = "//section/main/div/header/section/ul/li[3]/a/span"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 2")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', '', status) # удаление пробелов из числа подписок
    if int(status) > acc_subcriptions:
        print(j, "У аккаунта слишком много подписок")
        continue

    # 3. не должно быть ссылки на сайт
    element = "//section/main/div/header/section/div[2]/a"
    if xpath_existence(element) == 1:
        print(j, "Есть ссылка на сайт")
        continue

    # 4. проверка на наличие заданного числа публикаций
    element = "//section/main/div/header/section/ul/li[1]/a/span"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 4")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', '', status) # удаление пробелов из числа публикаций
    if int(status) < publications:
        print(j, "У аккаунта слишком мало публикаций")
        continue

    # 5. проверка на наличие аватара
    element = "//section/main/div/header/div/div/span/img"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 5")
        continue
    status = browser.find_element_by_xpath(element).get_attribute("src")
    if status.find("s150x150") == -1:
        print(j, "Профиль без аватара")
        continue

    '''#6. проверка даты последней публикации
    element = "//a[contains(@href, '/p/')]"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 6")
        continue
    status = browser.find_element_by_xpath(element).get_attribute("href")
    browser.get(status)
    post_date = browser.find_element_by_xpath("//time").get_attribute("datatime")
    year = int(post_date[0:4])
    month = int(post_date[5:7])
    day = int(post_date[8:10])
    post_date = datetime(year, month, day)
    period = today - post_date
    if period.days > days_pub:
        print(j, "Последня публикация было слишком давно")
        continue'''

    # добавление пользователя в отфильтрованный файл
    filtered_list.append(follower)
    print(j, "Добавлен новый пользователь", follower)
    i += 1
    # выход из цикла
    if i > 2:
        break

# запись в файл
f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\\filtered_persons_list.txt", 'w')
for line in filtered_list:
    f.write(line)
f.close()
print("\nДобавлено", i, "пользователей")

browser.quit()