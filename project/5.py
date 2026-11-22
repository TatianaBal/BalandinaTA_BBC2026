a=int(input("выбери уровень(1-5):"))
if a==1:
    test_1=str(input("тестовая строка:"))
    #пРиВет_МИР
    a1=str(input("выбери: upper-сделать все буквы заглавными, lower-сделать все буквы строчными, capilazise-сделать первую букву заглавной, остальные строчными:"))
    if a1=='upper':
        print(test_1.upper())
    if a1=='lower':
        print(test_1.lower())
    if a1=='capitalize':
        print(test_1.capitalize())
    

if a==2:
    test_2=str(input("тестовая строка:"))
    #Ботать_это_круто._Очень_круто
    a2=str(input("выбери: find- позиция первого вхождения 'круто', replace-заменить слово 'круто' на другое слово, count-считает сколько раз подстрока встречается в стороке:"))
    if a2=='find':
        print(test_2.find("круто"))
    if a2=='replace':
        n=str(input("на какое слово меняем:"))
        print(test_2.replace("круто",n))
    if a2=='count':
        print(test_2.count("о"))


if a==3:
    #split-разбивает стороку на список подстрок по разделителю, join-собирает строку из списка,вставляя между строками разделитель 
    test_3=str(input("тестовая строка:"))
    #1,2,3,4
    b=test_3.split(",")
    print(b)
    print("-".join(b))

if a==4:
    test_4_a=str(input("тестовая строка:"))
    #1234*&%$
    test_4_b=str(input("тестовая строка:"))
    #"    abc1234   "
    a4=str(input("выбери: isdigit-проверка, сотоит ли текст только из цифр, isalpha-проверяет, состоит ли строка только из букв, strip-убирает пробельные символы с обоих сторон страны, format:"))
    if a4=='isdigit':
        print(test_4_a.isdigit())
        print(test_4_b.isdigit())
    if a4=='isalpha':
        print(test_4_a.isalpha())
        print(test_4_b.isalpha())
    if a4=='strip':
        print(test_4_a.strip())
        print(test_4_b.strip())
    if a4=='format':
        #двигаем текст
        print(f"{test_4_a:>15}")
        print(f"{test_4_a:^15}")
        print(f"{test_4_a:<15}")
        #заменяем пробелы
        print(f"{test_4_a:*^12}")
        print(f"{test_4_b:->12}")
        print(f"{test_4_b:.<12}")
        #первые несколько символов
        print(f"{test_4_a:.5}")
if a==5:
    s='   pYtHon;is;AWESome:   '
    result=s.strip().replace(";"," ").replace(":","").lower()
    print(result)
    
    
        
        
