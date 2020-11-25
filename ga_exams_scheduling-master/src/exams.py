#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Exams for 1st year (1st semester)
exams1 = [
    'Cấu trúc dữ liệu và giải thuât',
    'OOP',
    'Đại số tuyến tính',
    'Nhập môn điện tử',
]

# Exams for 2nd year (3rd semester)
exams2 = [
    'Giải tích 2',
    'Phân tích thiết kế hệ thống thông tin',
    'Quản lý dự án công nghệ thông tin',
    'Cấu trúc rời rạc',
]

# Exams for 3rd year (5rd semester)
exams3 = [
    'Lập trình Java',
    'Lập trình web',
    'Hệ thống thông tin kế toán',
    'Oracle'
]

extra_exams = [
    'extra1',
    'extra2',
    # 'extra3',
    # 'extra4',
    # 'extra5',
    # 'extra6'
]

exams = exams1 + exams2 + exams3 + extra_exams

exams1_indexes = list(range(len(exams1)))

last_index = exams1_indexes[-1]
exams2_indexes = list(range(last_index+1, last_index+1+len(exams2)))

last_index = exams2_indexes[-1]
exams3_indexes = list(range(last_index+1, last_index+1+len(exams3)))

last_index = exams3_indexes[-1]
extra_exams_indexes = list(range(last_index+1, last_index+1+len(extra_exams)))
