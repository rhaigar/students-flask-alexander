

class Student:
    def __init__(self, id:int, name, email, phone):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f'{self.id},{self.name},{self.email},{self.phone}'
    

class Teacher:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f'{self.name},{self.email}'
    
class Course:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return f'{self.id},{self.name},{self.description}'
    

class Grade:
    def __init__(self, name, grade:int):
        self.name = name
        self.grade = grade

    def __str__(self):
        return f'{self.grade},{self.name}'
    
class Attend:
    def __init__(self, name, attend):
        self.name=name
        self.attend=attend

    def __str__(self):
        return f'{self.name},{self.attend}'