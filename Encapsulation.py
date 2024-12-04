class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return '������'

    def average_grade(self):
        if self.grades:
            return sum([sum(grades) for grades in self.grades.values()]) / sum(
                [len(grades) for grades in self.grades.values()])
        return 0

    def __str__(self):
        avg_grade = self.average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress)
        finished_courses = ', '.join(self.finished_courses)
        return (f'���: {self.name}\n'
                f'�������: {self.surname}\n'
                f'������� ������ �� �������� �������: {avg_grade:.1f}\n'
                f'����� � �������� ��������: {courses_in_progress}\n'
                f'����������� �����: {finished_courses}')

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.average_grade() < other.average_grade()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Student):
            return self.average_grade() > other.average_grade()
        return NotImplemented


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return '������'

    def __str__(self):
        return f'���: {self.name}\n�������: {self.surname}'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grade(self):
        if self.grades:
            return sum([sum(grades) for grades in self.grades.values()]) / sum(
                [len(grades) for grades in self.grades.values()])
        return 0

    def __str__(self):
        avg_grade = self.average_grade()
        return (f'���: {self.name}\n'
                f'�������: {self.surname}\n'
                f'������� ������ �� ������: {avg_grade:.1f}')

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.average_grade() < other.average_grade()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Lecturer):
            return self.average_grade() > other.average_grade()
        return NotImplemented


# ������� ��� �������� ������� ������
def average_student_grade(students, course):
    total_grades = 0
    count = 0
    for student in students:
        if course in student.grades:
            total_grades += sum(student.grades[course])
            count += len(student.grades[course])
    return total_grades / count if count > 0 else 0


def average_lecturer_grade(lecturers, course):
    total_grades = 0
    count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades += sum(lecturer.grades[course])
            count += len(lecturer.grades[course])
    return total_grades / count if count > 0 else 0


# �������� ����������� �������
student1 = Student('����', '������', '�������')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['�������� � ����������������']

student2 = Student('�����', '�������', '�������')
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ['�������� � ����������������']

reviewer1 = Reviewer('������', '�������')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('�����', '�������')
reviewer2.courses_attached += ['Git']

lecturer1 = Lecturer('���������', '�����')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('������', '�������')
lecturer2.courses_attached += ['Git']

# �������� ��������� ������
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Git', 8)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student1, 'Git', 10)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer1.rate_hw(student2, 'Git', 9)
reviewer1.rate_hw(student2, 'Python', 9)
reviewer1.rate_hw(student2, 'Git', 10)

# ������� ������ ������ ���������
student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Git', 8)
student2.rate_lecturer(lecturer1, 'Python', 6)
student1.rate_lecturer(lecturer1, 'Git', 8)
student1.rate_lecturer(lecturer2, 'Python', 8)
student1.rate_lecturer(lecturer2, 'Git', 7)
student2.rate_lecturer(lecturer2, 'Python', 10)
student1.rate_lecturer(lecturer2, 'Git', 8)

# ������� ������� ������
students = [student1, student2]
lecturers = [lecturer1, lecturer2]

avg_student_grade = average_student_grade(students, 'Python')
avg_lecturer_grade = average_lecturer_grade(lecturers, 'Python')


# ����� ����������
print(f'�������:\n{student1} \n')
print(f'�������:\n{student2} \n')
print(f'�������:\n{reviewer1} \n')
print(f'�������:\n{reviewer2} \n')
print(f'������:\n{lecturer1} \n')
print(f'������:\n{lecturer2} \n')

print(f'\n������� ������ ��������� �� ������ Python: {avg_student_grade:.1f}')
print(f'������� ������ �������� �� �������� �������: {avg_lecturer_grade:.1f}')

# ��������� ��������� � ��������
print(f'\n��������� ���������:')
if student1 > student2:
    print(f'{student1.surname} {student1.name} ����� ��� {student2.surname} {student2.name}')
if student2 > student1:
    print(f'{student2.surname} {student2.name} ����� ��� {student1.surname} {student1.name}')

print(f'\n��������� ��������:')
if lecturer1 > lecturer2:
    print(f'{lecturer1.surname} {lecturer1.name} ����� ��� {lecturer2.surname} {lecturer2.name}')
if lecturer2 > lecturer1:
    print(f'{lecturer2.surname} {lecturer2.name} ����� ��� {lecturer1.surname} {lecturer1.name}')