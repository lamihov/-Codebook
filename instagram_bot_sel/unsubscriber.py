from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time # модуль работы с временем

# Время между отписками
unsub_time = 3
# Кол-во отписок
max = 20

browser = webdriver.Chrome("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\chromedriver.exe") # переменная для работы с браузером


# Функция проверки существования элемента на странице
def xpath_existance(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


browser.get('https://www.instagram.com/')
# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/") # переход на страницу авторизации
time.sleep(3) # задаем время для прогрузки страницы
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys("test") # метод(блок формы в xPatch).ввод логина
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys("12345") # метод(блок формы в xPatch).ввод пароля
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button").click() # вход
time.sleep(5) # задаем время для прогрузки страницы

# Лист с моими подписчиками
file_list = []
f1 = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\my_subscriptions.txt", "w")
for line in f1:
    file_list.append(line)
f1.close()

# Процесс отписки
i = 0
for line in file_list:
    i += 1
    if i == max + 1:
        break
    browser.get(line)
    element = "//div/div/span/span[1]/button"
    if xpath_existance(element) == 0:
        print('Ошибка 1 поиска кнопки отписки')
        continue
    try:
        button = browser.find_element_by_xpath(element)
    except StaleElementReferenceException:
        print('Ошибка 2 поиска кнопки отписки')
        continue

    if button.text == 'Подписки':
        try:
            button.click()
        except StaleElementReferenceException:
            print("Ошибка 3 нажатия кнопки отписки")
            continue

    sleep(0.5)
    element = "//body/div[3]/div/div/div[3]/button[1]"
    if xpath_existance(element) == 0:
        print("Ошибка 4 нажатия кнопки отписки")
        continue
    button = browser.find_element_by_xpath(element)
    try:
        button.click()
    except StaleElementReferenceException:
        print("Ошибка 5 нажатия кнопки отписки")
        continue
    print("Произвелась отписка от", line)
    sleep(unsub_time)

# Очистка списка моих подписок
f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\my_subscriptions.txt", "w")
i = 0
for i in range(max, len(file_list)):
    f.write(file_list[i])
    i += 1
f.close()

# Завершение работы
browser.quit()