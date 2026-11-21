a=int(input("введите первое число:"))
b=int(input("введите второе число"))
c=str(input("знак операции:"))
def f(a,b):
    '''сложение'''
    print(a+b)
def g(a,b):
    '''вычитание'''
    print(a-b)
def d(a,b):
    '''умножение'''
    print(a*b)
def e(a,b):
    '''деление'''
    print(a/b)
if c=='+':
    print(f(a,b))
if c=='-':
    print(g(a,b))
if c=='*':
    print(d(a,b))
if c=='/':
    print(e(a,b))
    
    
        
    
        
    
