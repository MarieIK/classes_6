class Student:  # класс Студент
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.average_grade = 0  # средняя оценка за все ДЗ

    def add_courses(self, course_name):  # пополняем список завершенных курсов и удаляем его из текущих
        self.finished_courses.append(course_name)
        self.courses_in_progress.remove(course_name)

    def rate_lecturer(self, lecturer, course, grade):  # оцениваем лектора
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached \
                and 1 <= grade <= 10:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Проверьте правильность введенных данных'

    def get_average_rate(self):  # получаем среднюю оценку студента по всем курсам
        total, count = 0, 0
        for v in self.grades.values():
            total += sum(v)
            count += len(v)
        try:
            self.average_grade = round((total / count), 1)
        except ZeroDivisionError:
            return 0
        return self.average_grade

    def __str__(self):  # переопределяем магический метод __str__
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за домашние задания: {self.get_average_rate()}\n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)}\n'

    def __lt__(self, other):  # реализуем возможность сравнения через операторы сравнения
        if not isinstance(other, Student):
            print('Ошибка! Вы пытаетесь сравнить не студента!')
        else:
            if self.get_average_rate() > other.get_average_rate():
                print(f'Студент {self.name} усваивает материал лучше, чем {other.name}')
            else:
                print(f'Студент {other.name} усваивает материал лучше, чем {self.name}')


class Mentor:  # класс Ментор(родительский)
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):  # класс Лектор
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.average_grade = 0  # средняя оценка за все лекции

    def get_average_rate(self):  # получаем среднюю оценку от студентов по всем лекциям
        total, count = 0, 0
        for v in self.grades.values():
            total += sum(v)
            count += len(v)
        try:
            self.average_grade = round((total / count), 1)
        except ZeroDivisionError:
            return 0
        return self.average_grade

    def __str__(self):  # переопределяем магический метод __str__
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Средняя оценка за лекции: {self.get_average_rate()}\n'

    def __lt__(self, other):  # реализуем возможность сравнения через операторы сравнения
        if not isinstance(other, Lecturer):
            print('Ошибка! Вы пытаетесь сравнить не лектора!')
        else:
            if self.get_average_rate() > other.get_average_rate():
                print(f'Лектор {self.name} объясняет материал лучше, чем {other.name}')
            else:
                print(f'Лектор {other.name} объясняет материал лучше, чем {self.name}')


class Reviewer(Mentor):  # класс Ревьюер
    def rate_student(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Проверьте правильность введенных данных'

    def __str__(self):  # переопределяем магический метод __str__
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n'


def average_grade_stud(students, course):  # получаем среднюю оценку среди всех студентов по одному курсу
    total, count = 0, 0
    for st in students:
        total += sum(st.grades[course])
        count += len(st.grades[course])
    try:
        round((total / count), 1)
    except ZeroDivisionError:
        return 0
    return round((total / count), 1)


def average_grade_lec(lectures, course):  # получаем среднюю оценку среди всех лекторов по одному курсу
    total, count = 0, 0
    for lec in lectures:
        total += sum(lec.grades[course])
        count += len(lec.grades[course])
    try:
        round((total / count), 1)
    except ZeroDivisionError:
        return 0
    return round((total / count), 1)


peter = Student('Peter', 'Parker', 'male')
peter.courses_in_progress += ['Python', 'Java']

miron = Student('Miron', 'Gras', 'male')
miron.courses_in_progress += ['Python', 'Java', 'Go']

mike = Reviewer('Mike', 'Global')
mike.courses_attached += ['Python']
mike.rate_student(peter, 'Python', 5)

bruce = Reviewer('Bruce', 'Norton')
bruce.courses_attached += ['Java']
bruce.rate_student(peter, 'Java', 10)

shon = Lecturer('Shon', 'Conor')
shon.courses_attached += ['Java', 'Go', 'JS']

bob = Lecturer('Bob', 'Tornton')
bob.courses_attached += ['Java', 'C++']

peter.rate_lecturer(shon, 'Java', 8)
miron.rate_lecturer(shon, 'Java', 9)
miron.rate_lecturer(bob, 'Java', 10)

bruce.rate_student(miron, 'Java', 7)

print(f'Мирон до завершения курса:')
print(miron)

print(f'Мирон после завершения курса:')
miron.add_courses('Go')
print(miron)
print(peter)
print(mike)
print(shon)
print(bob)

print('Сравниваем студентов и лекторов по средней оценке:')
peter.__lt__(miron)
shon.__lt__(bob)

all_students = [peter, miron]
all_lectures = [shon, bob]
print()

print('Средняя оценка по курсу "Java"')
print(f'Среди студентов: {average_grade_stud(all_students, "Java")}')
print(f'Среди лекторов: {average_grade_lec(all_lectures, "Java")}')
