class Employee:
    num_of_emp=0
    raise_amount=1.03

    def __init__(self,first,last,pay):
        self.first=first
        self.last=last
        self.email=first+'.'+last+'@email.com'
        self.pay=pay
        self.num_of_emp=+1

    def apply_raise(self):
      self.pay=int(self.pay*self.raise_amount)

    def fullname(self):
        return '{} {}'.format(selft.first,self.last)

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount=amount

    @classmethod
    def from_str(cls,emp_str):
        first,last,pay=emp_str.split('-')
        return cls(first,last,pay)



# Example
emp1=Employee('Ray','Yang',6000)
emp2=Employee('Patrick','Yang',9000)
Employee.raise_amount=1.01

#
emp3_str='chin-Yang-10000'
emp3=Employee.from_str(emp3_str)
print(emp3.email)

print(emp1.fullname)
emp1.raise_amount=1.05
print(emp1.raise_amount)
print(emp2.raise_amount)
