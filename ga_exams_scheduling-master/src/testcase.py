#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exams import exams, exams1_indexes, exams2_indexes, exams3_indexes, extra_exams_indexes


# Number of students for particular year
students1 = 10
students2 = 7
students3 = 6

# Maps year to list of students (each student is represented as a list of exams)
students_exams = {
    1: [exams1_indexes[:] for _ in range(students1)],
    2: [exams2_indexes[:] for _ in range(students2)],
    3: [exams3_indexes[:] for _ in range(students3)],
}
# Tạo các exam cho từng khối, đánh số cho student exam theo thứ tự
# Introducing real life situations that some students from year 2 and 3 didn't pass
# exams from previous year


# 10 students didn't pass 'OOP 1'
physics_exam = exams.index('OOP')
for i in range(5):
    students_exams[2][i].append(physics_exam)

# 5 students didn't pass 'Giải tích 2'
physics_exam = exams.index('Giải tích 2')
for i in range(2):
    students_exams[3][i].append(physics_exam)


extra_exams_count = len(extra_exams_indexes)
# each student has 2 extra subjects exams
for student_year in students_exams.keys():
    for student_index, student_exams_list in enumerate(students_exams[student_year]):
        first_exam_index = student_index % (extra_exams_count-1)
        second_exam_index = first_exam_index + 1

        student_exams_list.append(extra_exams_indexes[first_exam_index])
        student_exams_list.append(extra_exams_indexes[second_exam_index])
