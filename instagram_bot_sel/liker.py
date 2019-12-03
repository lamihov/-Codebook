from selenium import webdriver # импорт вебдрайвера
import time # модуль работы с временем
import random # модуль для генерации случайных чисел
random.seed # инициализация генератора случайных чисел

# параметры

like_time = 10 # время между лайками
all_likes = 720 # максимальное количество количество лайков в сутки
all_subscriptions = 720 # максимальное количество подписок в сутки
hour_like = 30 # максимальное количество лайков в час
hour_sub = 30 # максимальное количество подписок в час

# в часе уже есть
likes = 0
subscriptions = 0


from selenium.common.exceptions import NoSuchElementException # исключения для отсутствия элемента
from selenium.common.exceptions import StaleElementReferenceException # исключение для устаревшего элемента
from selenium.common.exceptions import ElementClickInterceptedException # исключение для клика


# функция существования элеммента на странице
def xpath_existence (url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence

browser = webdriver.Chrome("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\chromedriver.exe") # переменная для работы с браузером

# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/") # переход на страницу авторизации
time.sleep(3) # задаем время для прогрузки страницы
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys("test") # метод(блок формы в xPatch).ввод логина
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys("12345") # метод(блок формы в xPatch).ввод пароля
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button").click() # вход
time.sleep(5) # задаем время для прогрузки страницы

# считывание отфильтрованных пользователей
f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\\filtered_persons_list.txt", "r")
file_list = []
for line in f:
    file_list.append(line)
f.close()

# считывание листа с существующими подписками
subscriptions_list = []
f1 = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\\my_subscriptions.txt", "r")
for line in f1:
    subscriptions_list.append(line)
f1.close()

j = 0 # номер вывода в терминале
n = 0 # пропущенное число пользователей из-за совпадения в subscriptions_listъ
next_person = 0 # если true - следующий пользователь по циклу
start_time = time.time() # время начала цикла

for person in file_list:

    # условие для паузы цикла
    if likes >= all_likes:
        print("Максимальное количество лайков за сутки")
        break
    if subscriptions >= all_subscriptions:
        print("Максимальное количество подписок за сутки")
        break
    # максимальное число подписок в час
    if ((time.time() - start_time) <= 60*60) and (hour_sub <= subscriptions):
        print("Предел числа подписок в час")
        print("Подождите", int ((60*60 - (time.time() - start_time))/60), "мин.")

        # удаление из отфильтрованных пользователей тех, на которых уже произвелась подписка
        f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\\filtered_persons_list.txt", 'w')
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.sleep(60 * 60 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0

    # максимальное число лайков в час
    if ((time.time() - start_time) <= 60*60) and (hour_sub <= likes):
        print("Предел числа лайков в час")
        print("Подождите", int ((60*60 - (time.time() - start_time))/60), "мин.")

        # удаление из отфильтрованных пользователей тех, на которых уже произвелась подписка
        f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\\filtered_persons_list.txt", 'w')
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.sleep(60 * 60 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0

    # обнуление часа
    if ((time.time() - start_time) >= 60*60):
        start_time = time.time()
        subscriptions = 0
        likes = 0

    # сравнение с массивом подписок
    for line in subscriptions_list:
        next_person = 0
        if person == line:
            next_person = 1
            print(j + 1, "\tПодписка на этого человека уже есть")
            j += 1
            n += 1
            break
    if next_person == 1:
        continue

    # вывод в терминал номера
    j += 1
    print("\n" + str(j -n) + ": ")

    # открытие страницы пользователя
    browser.get(person)
    time.sleep(1.5)

    # 1. открытие публикаций и лайки

    # проверка есть ли уже подписка на этого пользователя
    element = "//section/main/div/header/section/div[1]/a/button"
    if xpath_existence(element) == 1:
        try:
            follow_status = browser.find_element_by_xpath(element).text
        except: StaleElementReferenceException
            print(j, "Ошибка, код ошибки 1.1")
            continue
        if (follow_status == "Following") or follow_status (follow_status == "Подписки"):
            print("Вы уже подписаны на этого человека")
            continue

    # поиск публицкаций и открытие двух случайных публикаций
    element = "//a[contains(@href, '/p')]"
    if xpath_existence(element) == 0:
        print(j, "Ошибка, код ошибки: 1.2")
        continue
    post = browser.find_element_by_xpath(element)
    i = 0
    for post in posts:
        posts[i] = post.get_attribute("href")
        i += 1
    rand_post = random.randint(0, 5) # случайный 1 - 6 пост
    for i in range(2):
        browser.get(posts[rand_post + i])
        time.sleep(0.3)
        browser.find_element_by_xpath("//section/main/div/div/article/div[2]/section[1]//span[1]/button").click() # нажатие лайка
        likes += 1
        print("+1 лайк")
        time.sleep(like_time)

    # 2 Подписка на пользователя
    try:
        element = "/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button"
        if xpath_existence(element) == 0:
            print(j, "Ошибка, код ошибки: 2.0")
        try:
            browser.find_element_by_xpath(element).click
        except StaleElementReferenceException:
            print(j, "Ошибка, код ошибки: 2.1")
            continue
    except ElementClickInterceptedException:
        print(j, "Ошибка, код ошибки: 2.2")
        continue

    subscriptions += 1
    print("+1 Подписка", person[0:len(person) - 1])
    time.sleep(0.5)

    # запись новой подписки в файл подписок
    f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\my_subscriptions.txt", "a")
    f.write(person)
    f.close()
# конец цикла

# завершение работы
browser.quit()