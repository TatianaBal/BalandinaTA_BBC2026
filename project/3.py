a=int(input("введите первое число:"))
b=int(input("введите второе число"))
c=str(input("знак операции:"))
def f(a,b):
    if c=='+':
        print(a+b)
    if c=='-':
        print(a-b)
    if c=='*':
        print(a*b)
    if c=='/':
        print(a/b)
print(f(a,b))
