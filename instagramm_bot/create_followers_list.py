from selenium import webdriver # импорт вебдрайвера
import time # модуль работы с временем

browser = webdriver.Chrome("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\chromedriver.exe") # переменная для работы с браузером
browser.get("https://www.instagram.com/") # открытие ссылки в браузере

amount_followers = 120 # необходимое количество подписчиков

# вход в аккаунт
browser.get("https://www.instagram.com/accounts/login/") # переход на страницу авторизации
time.sleep(3) # задаем время для прогрузки страницы
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys("test") # метод(блок формы в xPatch).ввод логина
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys("12345") # метод(блок формы в xPatch).ввод пароля
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button").click() # вход
time.sleep(3) # задаем время для прогрузки страницы

# алгоритм действий
browser.get("https://www.instagram.com/radislavgandapas/") # переход на страницу блогера
time.sleep(3) # задаем время для прогрузки страницы

browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a").click() # открытие списка подписчиков
time.sleep(5) #задаем время для прогрузки страницы

scroll_element = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]") # создание элемента прокрутки
time.sleep(5) # задаем время для прогрузки страницы

browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %6, scroll_element) # осуществление прокрутки 1/6 страницы
time.sleep(0.9) # задаем время для прогрузки страницы
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %4.2, scroll_element) # осуществление прокрутки 1/4 страницы
time.sleep(0.8) # задаем время для прогрузки страницы
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %3, scroll_element) # осуществление прокрутки 1/3 страницы
time.sleep(1) # задаем время для прогрузки страницы
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %2.5, scroll_element) # осуществление прокрутки 1/2 страницы
time.sleep(1) # задаем время для прогрузки страницы
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %1.7, scroll_element) #осуществление прокрутки 1/2 страницы
time.sleep(1) # задаем время для прогрузки страницы

links_followers = [] # массив для хранения ссылок на подписчиков
t = 1.13 # значение времени прокрутки
num_scroll = 0 # количество прокруток
k = 0 # коэффициент ожидания

while len(links_followers) < amount_followers:
    num_scroll += 1
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_element)

    if num_scroll %10 == 0:
        print("!")
        # сохранение ссылок в links_followers
        followers = browser.find_elements_by_xpath("//div[@role='dialog']/div[2]/ul/div/li/div/div/div/div/a[@title]")
        for i in range(len(followers)):
            links_followers.append(str(followers[i].get_attribute('href')))
    time.sleep(t)

    # ожидание для обхода фильтров
    if (len(links_followers) > (2000 + 1000*k)):
        print ("\nОжидание 10 минут")
        time.sleep(600)
        p += 1

# создание файла со списком пользователей
f = open("D:\YG\Программирование\Python\Практика\Codebook\insta_bot\massiv.txt", 'w')
for follower in links_followers:
    f.write(follower)
    f.write("\n")
f.close

# закрытие браузера
browser.quit()