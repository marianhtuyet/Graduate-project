import xlsxwriter
from odoo import models


class StudyclassReportXlsxTemplate(models.AbstractModel):
    _name = 'report.student_score_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        self.company = self.env.user.company_id
        self.scholar_year = objs.school_year_id.name
        self.line_ids = objs.study_class_ids
        self.wb = workbook

        self.obj = objs
        print('objs', objs)
        self.sheet_name = 'Transcript of record'
        self.sheet = self.wb.add_worksheet(self.sheet_name)
        self.sheet.insert_image(
            'A1',
            'C:/odoo_project/custom_addons/Caculate_score/report/logo.jpg',
            {'x_offset': 100, 'y_offset': 0}
        )
        self._set_cells_size()
        self._define_format()
        self.generate_template_header()
        self.generate_footer()

    def _set_cells_size(self):
        self.sheet.set_column('A:A', 25)
        self.sheet.set_column('B:D', 8)
        self.sheet.set_column('E:E', 3)
        self.sheet.set_column('F:F', 25)
        self.sheet.set_column('G:I', 8)
        self.row_pos = 6

    def generate_template_header(self):
        self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
                               'TRANSCRIPT OF RECORD', self.bold_center_16)
        self.row_pos += 1
        self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
                               'Theological cycle: '.format(self.obj.school_year_id.name), self.bold_center)
        self.row_pos += 2
        self.sheet.merge_range(
            'A{}:D{}'.format(self.row_pos, self.row_pos),
            'Name: {}'.format(self.obj.name),
            self.bold_left
        )
        self.sheet.merge_range(
            'F{}:I{}'.format(self.row_pos, self.row_pos),
            'POB: {}'.format(self.obj.position_of_birth),
            self.bold_left
        )
        self.row_pos += 1
        self.sheet.merge_range(
            'A{}:D{}'.format(self.row_pos, self.row_pos),
            'DOB: {}'.format(self.obj.date_of_birth),
            self.bold_left
        )
        self.sheet.merge_range(
            'F{}:I{}'.format(self.row_pos, self.row_pos),
            'Congregation: {}'.format(self.obj.congregation),
            self.bold_left
        )
        self.row_pos += 2
        scholar_year = self.scholar_year.split('-')
        start_year = self.scholar_year.date_start.year
        end_year = self.scholar_year.date_start.year
        temp = end_year - start_year
        list_scholar_year = []
        total_units = sum(line.units for line in self.line_ids)
        avg_total_unit = sum(line.grade_point for line in self.line_ids) / total_units if total_units > 0 else 1
        for x in range(temp):
            list_scholar_year.append('{} - {}'.format(int(scholar_year[0]), int(scholar_year[0]) + x + 1))
        count_row, max_count_row = 0, 0
        list_columns = [['A', 'B', 'C', 'D'], ['F', 'G', 'H', 'I']]
        for x in range(temp):
            if x % 2 == 0:
                count_row = self.row_pos
                self.generate_header(self.row_pos, list_columns[0], list_scholar_year[x])
                self.row_pos += 1
                self.generate_one_semmeter(
                    self.line_ids.filtered(lambda m: m.subject_id.sequence == x + 1),
                    list_columns[0],
                    count_row + 1 if x < 2 else max_count_row + 1,
                    max_count_row
                )
                max_count_row = self.row_pos + 1
            else:
                self.generate_header(
                    count_row if x < 2 or (x > 2 and x % 2 != 0) else max_count_row + 1,
                    list_columns[1], list_scholar_year[x])
                self.row_pos += 1
                self.generate_one_semmeter(
                    self.line_ids.filtered(lambda m: m.subject_id.sequence == x + 1),
                    list_columns[1],
                    count_row + 1 if x < 2 or (x > 2 and x % 2 != 0) else max_count_row + 1,
                    max_count_row,
                    is_last=True if x == temp - 1 else False
                )
                self.row_pos = max(max_count_row, self.row_pos)


    def generate_header(self, start_line, list_column, list_scholar_year):
        self.row_pos = start_line
        self.xlsx_write(
            list_column[0],
            '{}: Subject'.format(list_scholar_year),
            self.border_header_left_6,
        )
        self.xlsx_write(
            list_column[1],
            'Units',
            self.border_header_top_bottom_6,
        )
        self.xlsx_write(
            list_column[2],
            'Grade \n point',
            self.border_header_top_bottom_6,
        )
        self.xlsx_write(
            list_column[3],
            'Qualifi\ncation',
            self.border_header_right_6,
        )

    def generate_one_semmeter(
            self, line_ids, list_column, start_line, max_row_count=0, is_last=False,
            total_units=0, avg_total_unit=0):
        print('start_line:   ', start_line)
        self.row_pos = start_line
        total_unit = 0
        for line in line_ids:
            self.xlsx_write(
                list_column[0],
                line.subject_id.name2,
                self.border_left_6,
            )
            self.xlsx_write(
                list_column[1],
                line.units,
                self.border_10,
            )
            self.xlsx_write(
                list_column[2],
                line.grade_point,
                self.border_10,
            )
            self.xlsx_write(
                list_column[3],
                line.qualification,
                self.border_right_6,
            )
            self.row_pos += 1
            total_unit += line.units
        if self.row_pos < max_row_count:
            self.xlsx_merge_range(
                '{}{}:{}{}'.format(
                    list_column[0],
                    self.row_pos,
                    list_column[0],
                    max_row_count - 2 if not is_last else self.row_pos + 2),
                'WEIGHTED AVERAGE',
                self.border_left_bottom_6,
            )
            self.xlsx_merge_range(
                '{}{}:{}{}'.format(
                    list_column[1],
                    self.row_pos,
                    list_column[1],
                    max_row_count - 2 if not is_last else self.row_pos+2),
                total_unit,
                self.border_bottom_6,
            )
            self.xlsx_merge_range(
                '{}{}:{}{}'.format(
                    list_column[2],
                    self.row_pos,
                    list_column[2],
                    max_row_count - 2 if not is_last else self.row_pos+2),
                '',
                self.border_bottom_6,
            )
            self.xlsx_merge_range(
                '{}{}:{}{}'.format(
                    list_column[3],
                    self.row_pos,
                    list_column[3],
                    max_row_count - 2 if not is_last else self.row_pos+2),
                '',
                self.border_right_bottom_6,
            )
        else:
            self.xlsx_write(list_column[0], 'WEIGHTED AVERAGE ', self.border_left_bottom_6)
            self.xlsx_write(list_column[1], total_unit, self.border_bottom_6)
            self.xlsx_write(list_column[2], '', self.border_bottom_6)
            self.xlsx_write(list_column[3], '', self.border_right_bottom_6)
        self.row_pos +=1
        if is_last:
            self.row_pos += 2
            self.print_summary_line(list_column, total_units, avg_total_unit)


    def print_summary_line(self, list_column,  total_units=0, avg_total_unit=0):
        self.xlsx_write(list_column[0], 'TOTAL WEIGHTED AVERAGE', self.border_left_6)
        self.xlsx_write(list_column[1], total_units, self.border_10)
        self.xlsx_write(list_column[2], '', self.border_10)
        self.xlsx_write(list_column[3], '', self.border_right_6)
        self.row_pos +=1
        self.xlsx_write(list_column[0], 'GRADUATION TEST', self.border_left_6)
        self.xlsx_write(list_column[1], avg_total_unit, self.border_10)
        self.xlsx_write(list_column[2], '', self.border_10)
        self.xlsx_write(list_column[3], '', self.border_right_6)
        self.row_pos +=1
        self.xlsx_write(list_column[0], 'FINAL GRADE', self.border_left_bottom_6)
        self.xlsx_write(list_column[1], '', self.border_bottom_6)
        self.xlsx_write(list_column[2], '', self.border_bottom_6)
        self.xlsx_write(list_column[3], '', self.border_right_bottom_6)

    def generate_footer(self):
        self.row_pos += 1
        self.xlsx_merge_range(
            'A{}:I{}'.format(self.row_pos, self.row_pos),
            '-'*200,
            self.normal_center_10
        )
        self.row_pos +=1
        self.sheet.set_row(self.row_pos-1, 30)
        self.xlsx_merge_range(
            'A{}:I{}'.format(self.row_pos, self.row_pos),
            'NB. The evaluating way is basically relied on the Grade point system of UST: E-Excellent(1.00-1.20)'
            ', VG-Very Good(1.21-1.45);    \n G-Good(1.46-1.85), F-Fair(1.86-2.40), P-Passed(2.41-3.00), F-Failure(below 3.00).',
            self.normal_left_10
        )
    def _define_format(self):
        self.normal_center_10 = self.wb.add_format({
            'align': 'center',
            'valign': 'top',
            'font_size': 10,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.normal_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.normal_center14 = self.wb.add_format({
            'text_wrap': True,
            'align': 'center',
            'valign': 'top',
            'font_size': 14,
            'font_name': 'Times New Roman',
        })

        self.bold_center = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })

        self.bold_center_16 = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })

        self.bold_center_border = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'border': 1,
            'font_name': 'Times New Roman',
        })
        self.bold_center13 = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'top',
            'font_size': 13,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.bold_center14 = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'top',
            'font_size': 14,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.bold_left_10 = self.wb.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'top',
            'font_size': 10,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.bold_left = self.wb.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'top',
            'font_size': 12,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_bot = self.wb.add_format({
            'bottom': 1,
        })

        self.border_header_left_6 = self.wb.add_format({
            'left': 6,
            'top':6,
            'bottom':6,
            'right':1,
            'align': 'left',
            'valign': 'top',
            'font_size': 12,
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_header_right_6 = self.wb.add_format({
            'right': 6,
            'top': 6,
            'bottom': 6,
            'left':1,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_header_top_bottom_6 = self.wb.add_format({
            'left':1,
            'right': 1,
            'top': 6,
            'bottom': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_top_bottom_6 = self.wb.add_format({
            'left': 1,
            'right': 1,
            'top': 6,
            'bottom': 6,
            'border': 1,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_left_6 = self.wb.add_format({
            'border': 1,
            'left': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 10,
            'font_name': 'Times New Roman',
        })
        self.border_right_6 = self.wb.add_format({
            'border': 1,
            'right': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 10,
            'font_name': 'Times New Roman',
        })
        self.border_bottom_6 = self.wb.add_format({
            'border': 1,
            'bottom': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 10,
            'font_name': 'Times New Roman',
        })
        self.border_10 = self.wb.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 10,
            'font_name': 'Times New Roman',
        })
        self.border_left_bottom_6 = self.wb.add_format({
            'left': 6,
            'right': 1,
            'top': 1,
            'bottom': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
        self.border_right_bottom_6 = self.wb.add_format({
            'left': 1,
            'right': 6,
            'top': 1,
            'bottom': 6,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_name': 'Times New Roman',
        })
