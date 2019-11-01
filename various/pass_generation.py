#генератор паролей
from random import sample
array = []
symbol = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYxzZ@#$%&=-+.?!*0123456789"

array.append(sample(symbol,10))
string = str(array)
password = string.replace(", ", "").replace("'", "").replace("]", "").replace("[", "")
print(password)