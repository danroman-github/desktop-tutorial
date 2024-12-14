class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []  # Список завершенных курсов
        self.courses_in_progress = []  # Список курсов в процессе изучения
        self.grades = {}  # Оценки по курсам

    @staticmethod
    def calculate_average(grades):
        """Вычисляет среднюю оценку для студента."""
        all_grades = [grade for grades_list in grades.values() for grade in grades_list]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def rate_lecturer(self, lecturer, course, grade):
        """Оценивает лектора."""
        if not (1 <= grade <= 10):
            raise ValueError("Оценка должна быть в диапазоне от 1 до 10.")
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            raise ValueError("Некорректные данные для оценки лектора.")

    def average_grade(self):
        """Возвращает среднюю оценку студента."""
        return self.calculate_average(self.grades)

    def __str__(self):
        """Форматирует информацию о студенте для вывода."""
        avg_grade = self.average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {avg_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress}\n"
                f"Завершенные курсы: {finished_courses}")

    def __lt__(self, other):
        """Сравнение студентов по средней оценке."""
        if isinstance(other, Student):
            return self.average_grade() < other.average_grade()
        return NotImplemented

    def __gt__(self, other):
        """Сравнение студентов по средней оценке."""
        if isinstance(other, Student):
            return self.average_grade() > other.average_grade()
        return NotImplemented


class Mentor:
    """Родительский класс Наставник для лекторов и экспертов."""
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []  # Курсы, к которым прикреплен ментор


class Reviewer(Mentor):
    """Класс Эксперт, который проверяет работу студентов."""
    def rate_hw(self, student, course, grade):
        """Оценивает студента."""
        if not (1 <= grade <= 10):
            raise ValueError("Оценка должна быть в диапазоне от 1 до 10.")
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            student.grades.setdefault(course, []).append(grade)
        else:
            raise ValueError("Некорректные данные для оценки студента.")

    def __str__(self):
        return f"Имя: {self.name} \ Фамилия: {self.surname}"


class Lecturer(Mentor):
    """Класс лектора, который проводит занятия и получает оценки от студентов."""
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    @staticmethod
    def calculate_average(grades):
        """Вычисляет среднюю оценку для лектора."""
        all_grades = [grade for grades_list in grades.values() for grade in grades_list]
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def average_grade(self):
        """Возвращает среднюю оценку лектора."""
        return self.calculate_average(self.grades)

    def __str__(self):
        """Форматирует информацию о лекторе для вывода."""
        avg_grade = self.average_grade()
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {avg_grade:.1f}")

    def __lt__(self, other):
        """Сравнение лекторов по средней оценке."""
        if isinstance(other, Lecturer):
            return self.average_grade() < other.average_grade()
        return NotImplemented

    def __gt__(self, other):
        """Сравнение лекторов по средней оценке."""
        if isinstance(other, Lecturer):
            return self.average_grade() > other.average_grade()
        return NotImplemented


# Создание экземпляров классов
student1 = Student("Иван", "Иванов", "мужской")
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ["Введение в программирование"]

student2 = Student("Мария", "Машкова", "женский")
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ["Введение в программирование"]

reviewer1 = Reviewer("Руслан", "Великов")
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer("Елена", "Петрова")
reviewer2.courses_attached += ['Git']

lecturer1 = Lecturer('Александр', 'Савин')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Кирилл', 'Сафонов')
lecturer2.courses_attached += ['Git']

# Студенты оценивают лекции
reviewer1.rate_hw(student1, 'Python', 10)
reviewer2.rate_hw(student1, 'Git', 8)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer2.rate_hw(student1, 'Git', 10)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer2.rate_hw(student2, 'Git', 9)
reviewer1.rate_hw(student2, 'Python', 9)
reviewer2.rate_hw(student2, 'Git', 10)

# Лекторы ставят оценки студентам
student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer1, 'Python', 8)
student1.rate_lecturer(lecturer2, 'Git', 6)
student2.rate_lecturer(lecturer2, 'Git', 8)
student1.rate_lecturer(lecturer1, 'Python', 8)
student2.rate_lecturer(lecturer1, 'Python', 7)
student1.rate_lecturer(lecturer2, 'Git', 10)
student2.rate_lecturer(lecturer2, 'Git', 8)

# Вывод информации
print(f"Студент:\n{student1} \n")
print(f"Студент:\n{student2} \n")
print(f"Эксперт:\n{reviewer1} \n")
print(f"Эксперт:\n{reviewer2} \n")
print(f"Лектор:\n{lecturer1} \n")
print(f"Лектор:\n{lecturer2} \n")

# Сравнение студентов и лекторов
print(f"\nСравнение студентов:")
if student1 > student2:
    print(f"{student1.surname} {student1.name} лучше чем {student2.surname} {student2.name}")
if student2 > student1:
    print(f"{student2.surname} {student2.name} лучше чем {student1.surname} {student1.name}")

print(f"\nСравнение лекторов:")
if lecturer1 > lecturer2:
    print(f"{lecturer1.surname} {lecturer1.name} лучше чем {lecturer2.surname} {lecturer2.name}")
if lecturer2 > lecturer1:
    print(f"{lecturer2.surname} {lecturer2.name} лучше чем {lecturer1.surname} {lecturer1.name}")
