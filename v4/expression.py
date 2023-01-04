import math
import random
num = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

class exp:

    def random_choice():
        random_int = math.floor(random.random()* 10)
        return random_int

    def add():
        sum = 10
        while sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] != 0:
                sum = n[0] + n[1]
        expression = f'{n[0]} + {n[1]}'
        string = f'{num[n[0]]} plus {num[n[1]]}'
        return string, expression, sum
        
    def sub():
        sum = -1
        while sum < 0:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] != 0:
                sum = n[0] - n[1]
        expression = f'{n[0]} - {n[1]}'
        string = f'{num[n[0]]} minus {num[n[1]]}'
        return string, expression, sum
    
    def add_and_sub():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0:
                sum = n[0] + n[1] - n[2]
        expression = f'{n[0]} + {n[1]} - {n[2]}'
        string = f'{num[n[0]]} plus {num[n[1]]} minus {num[n[2]]}'
        return string, expression, sum

    def sub_and_add():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0:
                sum = n[0] - n[1] + n[2]
        expression = f'{n[0]} - {n[1]} + {n[2]}'
        string = f'{num[n[0]]} minus {num[n[1]]} plus {num[n[2]]}'
        return string, expression, sum

    def div_and_add():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0 and n[1] != 1:
                if n[0] % n[1] == 0 and n[0] != n[1]:
                    sum = n[0] / n[1] + n[2]
        expression = f'{n[0]} / {n[1]} + {n[2]}'
        string = f'{num[n[0]]} divided by {num[n[1]]} plus {num[n[2]]}'
        return string, expression, sum

    def div_and_sub():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0 and n[1] != 1:
                if n[0] % n[1] == 0 and n[0] != n[1]:
                    sum = n[0] / n[1] - n[2]
        expression = f'{n[0]} / {n[1]} - {n[2]}'
        string = f'{num[n[0]]} divided by {num[n[1]]} minus {num[n[2]]}'
        return string, expression, sum
    
    
    def multi_and_add():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0:
                if n[0] != 1 and n[1] != 1:
                    sum = n[0] * n[1] + n[2]
        expression = f'{n[0]} x {n[1]} - {n[2]}'
        string = f'{num[n[0]]} times {num[n[1]]} plus {num[n[2]]}'
        return string, expression, sum

    def multi_and_sub():
        sum = -1
        while sum < 0 or sum > 9:
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0:
                if n[0] != 1 and n[1] != 1:
                    sum = n[0] * n[1] - n[2]
        expression = f'{n[0]} x {n[1]} - {n[2]}'
        string = f'{num[n[0]]} times {num[n[1]]} minus {num[n[2]]}'
        return string, expression, sum
    

    def add_and_div():
        sum = -1
        while sum < 0 or sum > 9 or math.ceil(sum % 1):
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0 and n[1] != 1:
                if n[0] % n[1] == 0 and n[0] != n[1]:
                    sum = n[0] + n[1] / n[2]
        
        expression = f'{n[0]} + {n[1]} / {n[2]}'
        string = f'{num[n[0]]} plus {num[n[1]]} divided by {num[n[2]]}'
        return string, expression, sum

    def sub_and_div():
        sum = -1
        while sum < 0 or sum > 9 or math.ceil(sum % 1):
            n = [math.floor(random.random()* 10) for i in range(0,3)]
            if n[0] and n[1] and n[2] != 0 and n[1] != 1:
                if n[0] % n[1] == 0 and n[0] != n[1]:
                    sum = n[0] - n[1] / n[2]
        expression = f'{n[0]} - {n[1]} / {n[2]}'
        string = f'{num[n[0]]} minus {num[n[1]]} divided by {num[n[2]]}'
        return string, expression, sum


    # Levels
    def eazy(fist_exp, second_exp):
        if round(random.random()):
            return fist_exp
        else:
            return second_exp


    def hard():
        rand_int = math.floor(random.random()* 10)
        if rand_int < 1.5:
            return exp.eazy(exp.add_and_sub(), exp.sub_and_add())
        elif rand_int > 8.5:
            return exp.eazy(exp.sub_and_div(), exp.add_and_div())
        else:
            if round(random.random()):
                return exp.eazy(exp.multi_and_add(), exp.multi_and_sub())
            else:
                return exp.eazy(exp.div_and_add(), exp.div_and_sub())