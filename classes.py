

class Student:
    def __init__(self, id, name, email,):
        self.id =  id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f'{self.id},{self.name},{self.email}'
    

class Teacher:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    
    def __str__(self):
        return f'{self.id},{self.name},{self.email}'
    
class Course:
    def __init__(self, id, name):
        self.id = id
        self.name = name


    def __str__(self) -> str:
        return f'{self.id},{self.name},'
    

class Grade:
    def __init__(self, name, grade:int):
        self.name = name
        self.grade = grade

    
    def __str__(self) -> str:
        return f'{self.grade},{self.name}'
    
class Attend:
    def __init__(self, name, attend):
        self.name=name
        self.attend=attend

    def __str__(self) -> str:
        return f'{self.name},{self.attend}'