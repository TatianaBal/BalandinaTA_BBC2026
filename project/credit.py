class Credit:
    def __init__(self,amount,percent,years):
        self.amount=amount
        self.percent=percent
        self.years=years
    def payment(self):
        rate=self.percent/100/12#месячная ставка
        months=self.years*12
        payment=self.amount*rate/(1-(1+rate)**(-months))
        return payment
amount=float(input("сумма кредита:"))
percent=float(input("годовая процентная ставка:"))
years=int(input("на сколько лет:"))

credit=Credit(amount,percent,years)
print("платеж в месяц:", round(credit.payment(),2))
              
             
        
    
