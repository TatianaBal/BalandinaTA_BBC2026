
class Calculator:
    def h(self,a,b):
        '''сложение'''
        return(a+b)
    def g(self,a,b):
        '''вычитание'''
        return(a-b)
    def d(self,a,b):
        '''умножение'''
        return(a*b)
    def e(self,a,b):
        '''деление'''
        return(a/b)
calc=Calculator()
a=int(input("введите первое число:"))
b=int(input("введите второе число:"))
c=str(input("знак операции:"))

if c=='+':
    result=calc.h(a,b)
    print(f"{result}")
if c=='-':
    result=calc.g(a,b)
    print(f"{result}")
if c=='*':
    result=calc.d(a,b)
    print(f"{result}")
if c=='/':
    result=calc.e(a,b)
    print(f"{result}")
    
