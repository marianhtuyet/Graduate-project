from odoo import models


class StudyclassReportXlsxTemplate(models.AbstractModel):
    _name = 'report.student_score_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        self.company = self.env.user.company_id
        # self.date_from = objs.date_from
        # self.date_to = objs.date_to
        # self.account_ids = objs.account_ids
        self.scholar_year = objs.school_year_id.name
        self.line_ids = objs.study_class_ids
        self.wb = workbook
        wrap_format = workbook.add_format({'text_wrap': True})
        self.obj = objs[0]
        self.sheet_name = 'Transcript of record'
        self.sheet = self.wb.add_worksheet(self.sheet_name)
        self._set_cells_size()
        self._define_format()
        self.generate_template_header()
        self.generate_template_content()

    def _set_cells_size(self):
        self.sheet.set_column('A:A', 25)
        self.sheet.set_column('B:D', 8)
        self.sheet.set_column('E:E', 3)
        self.sheet.set_column('F:F', 25)
        self.sheet.set_column('G:I', 8)
        self.row_pos = 6

    def generate_template_header(self):
        self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
                               'TRANSCRIPT OF RECORD', self.bold_center_border)
        self.row_pos += 1
        self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
                               'Theological cycle: '.format(), self.bold_center_border)
        self.row_pos +=1
        scholar_year = self.scholar_year.split('-')



        temp = int(scholar_year[1]) - int(scholar_year[0])
        list_scholar_year = []
        for x in range(temp):
            list_scholar_year.append('{} - {}'.format(int(scholar_year[0]), int(scholar_year[0]) +x + 1))
        count_row, max_count_row = 0, 0

        list_columns = [['A', 'B', 'C', 'D'], ['F', 'G', 'H', 'I']]
        for x in range(temp):

            print(self.line_ids.filtered(lambda m: m.subject_id.sequence == x+1))
            if x % 2 == 0:
                count_row = self.row_pos
                self.generate_header(self.row_pos,list_columns[0], list_scholar_year[x])
                self.row_pos += 1
                self.generate_one_semmeter(
                    self.line_ids.filtered(lambda m: m.subject_id.sequence == x+1),
                    list_columns[0],
                    start_line =  count_row+1 if x <2 else max_count_row + 1
                )
                max_count_row = self.row_pos +1
            else:
                self.generate_header(
                    count_row if x <2 or (x >2 and x %2 != 0) else max_count_row + 1,
                    list_columns[1], list_scholar_year[x])
                self.row_pos += 1
                self.generate_one_semmeter(
                    self.line_ids.filtered(lambda m: m.subject_id.sequence == x + 1),
                    list_columns[1],
                    start_line =  count_row+1 if x <2 or (x >2 and x %2 != 0) else max_count_row + 1
                )
                self.row_pos = max(max_count_row, self.row_pos)
            print('count_row, self.row_pos:  ', count_row, self.row_pos)

    def generate_header(self, start_line, list_column, list_scholar_year):
        print('start_line header:   ', start_line)
        print('self.row_pos header:  ', self.row_pos)
        self.row_pos = start_line

        self.xlsx_write(
            list_column[0],
            '{}: Subject'.format(list_scholar_year),
            self.bold_left,
        )
        self.xlsx_write(
            list_column[1],
            'Units',
            self.bold_left,
        )
        self.xlsx_write(
            list_column[2],
            'Grade \n point',
            self.bold_left,
        )
        self.xlsx_write(
            list_column[3],
            'Qualifi\ncation',
            self.bold_left,
        )

    def generate_one_semmeter(self, line_ids, list_column, start_line):
        print('start_line:   ', start_line)
        print('self.row_pos:  ', self.row_pos)
        self.row_pos = start_line
        for line in line_ids:
            self.xlsx_write(
                list_column[0],
                line.subject_id.name,
                self.normal_left_10,
            )
            self.xlsx_write(
                list_column[1],
                line.units,
                self.normal_left_10,
            )
            self.xlsx_write(
                list_column[2],
                line.grade_point,
                self.normal_left_10,
            )
            self.xlsx_write(
                list_column[3],
                line.qualification,
                self.normal_left_10,
            )
            self.row_pos += 1

        # self.sheet.write('H{}'.format(self.row_pos), 'Mẫu số S07-DN',
        #                  self.bold_center14)
        # self.row_pos += 1
        # address = ''
        # if self.company.street:
        #     address += self.company.street
        # if self.company.street2:
        #     address += ', ' + self.company.street2
        # if self.company.city:
        #     address += ', ' + self.company.city
        # if self.company.country_id.name:
        #     address += ', ' + self.company.country_id.name
        # self.sheet.write(
        #     'A{}'.format(self.row_pos),
        #     'Địa chỉ: {}'.format(address),
        #     self.bold_left
        # self.sheet.write('H{}'.format(self.row_pos),
        #                  '(Ban hành theo Thông tư số 200/2014/TT-BTC\nNgày '
        #                  '22/12/2014 của Bộ Tài chính)', self.normal_center)
        # self.row_pos += 4
        # self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
        #                        'SỔ QUỸ TIỀN MẶT', self.bold_center14)
        # self.row_pos += 1
        # self.sheet.merge_range('A{}:I{}'.format(self.row_pos, self.row_pos),
        #                        'CASH BOOK', self.bold_center13)
        # self.row_pos += 1
        # account_no = ''
        # for code in self.account_ids.mapped('code'):
        #     account_no += code if not account_no else ' %s' % code
        # self.sheet.merge_range(
        #     'A{}:I{}'.format(self.row_pos, self.row_pos),
        #     'Tài khoản/ Account No.: {}'.format(account_no),
        #     self.normal_center)
        # self.row_pos += 1
        # self.sheet.merge_range(
        #     'A{}:I{}'.format(self.row_pos, self.row_pos),
        #     'Từ ngày/ From: {} đến ngày/to: {}'.format(self.date_from,
        #                                                self.date_to),
        #     self.normal_center)
        # self.row_pos += 3
        # self.sheet.merge_range('A{}:A{}'.format(self.row_pos, self.row_pos+2),
        #                        'Ngày ghi sổ\nPosted date',
        #                        self.bold_center_border)
        # self.sheet.merge_range('B{}:B{}'.format(self.row_pos, self.row_pos+2),
        #                        'Ngày chứng từ\nDate of vouchers',
        #                        self.bold_center_border)
        # self.sheet.merge_range('C{}:D{}'.format(self.row_pos, self.row_pos),
        #                        'Số hiệu chứng từ\nReference to',
        #                        self.bold_center_border)
        # self.sheet.write('C{}'.format(self.row_pos+1), 'Thu',
        #                  self.bold_center_border)
        # self.sheet.write('D{}'.format(self.row_pos+1), 'Chi',
        #                  self.bold_center_border)
        # self.sheet.write('C{}'.format(self.row_pos+2), 'Receivement',
        #                  self.bold_center_border)
        # self.sheet.write('D{}'.format(self.row_pos+2), 'Payment',
        #                  self.bold_center_border)
        # self.sheet.write('E{}'.format(self.row_pos), 'Diễn giải',
        #                  self.bold_center)
        # self.sheet.write('E{}'.format(self.row_pos-1), '', self.border_bot)
        # self.sheet.write('E{}'.format(self.row_pos+1), 'Descriptions',
        #                  self.bold_center)
        # self.sheet.merge_range('F{}:H{}'.format(self.row_pos, self.row_pos),
        #                        'Số tiền\nAmount', self.bold_center_border)
        # self.sheet.write('F{}'.format(self.row_pos+1), 'Thu',
        #                  self.bold_center_border)
        # self.sheet.write('G{}'.format(self.row_pos+1), 'Chi',
        #                  self.bold_center_border)
        # self.sheet.write('H{}'.format(self.row_pos+1), 'Tồn',
        #                  self.bold_center_border)
        # self.sheet.write('F{}'.format(self.row_pos+2), 'Receivement',
        #                  self.bold_center_border)
        # self.sheet.write('G{}'.format(self.row_pos+2), 'Payment',
        #                  self.bold_center_border)
        # self.sheet.write('H{}'.format(self.row_pos+2), 'Balance',
        #                  self.bold_center_border)
        # self.sheet.merge_range('I{}:I{}'.format(self.row_pos, self.row_pos+2),
        #                        'Ghi chú\nnotes', self.bold_center_border)
        # self.sheet.write('I{}'.format(self.row_pos+1), '',
        #                  self.bold_center_border)
        # self.sheet.write('I{}'.format(self.row_pos+2), '',
        #                  self.bold_center_border)
        # self.row_pos += 3
        # self.sheet.write('A{}'.format(self.row_pos), 'A',
        #                  self.bold_center_border)
        # self.sheet.write('B{}'.format(self.row_pos), 'B',
        #                  self.bold_center_border)
        # self.sheet.write('C{}'.format(self.row_pos), '',
        #                  self.bold_center_border)
        # self.sheet.write('D{}'.format(self.row_pos), '',
        #                  self.bold_center_border)
        # self.sheet.write('E{}'.format(self.row_pos), 'E',
        #                  self.bold_center_border)
        # self.sheet.write('F{}'.format(self.row_pos), '1',
        #                  self.bold_center_border)
        # self.sheet.write('G{}'.format(self.row_pos), '2',
        #                  self.bold_center_border)
        # self.sheet.write('H{}'.format(self.row_pos), '3',
        #                  self.bold_center_border)
        # self.sheet.write('I{}'.format(self.row_pos), 'G',
        #                  self.bold_center_border)
        # self.row_pos += 1

    def generate_template_content(self):
        # for line in self.objs.study_class_ids.filtered(lambda m: m.subject_id.sequence == x):
            print("*"*80)
        # for line in self.obj.get_move_lines(self.account_ids, self.date_from,
        #                                     self.date_to):
        #     self.sheet.write('A{}'.format(self.row_pos), str(line.date),
        #                      self.arial)
        #     self.sheet.write('B{}'.format(self.row_pos), str(line.date),
        #                      self.arial)
        #     self.sheet.write('C{}'.format(self.row_pos), line.debit
        #                      and line.payment_id.name or '',
        #                      self.arial)
        #     self.sheet.write('D{}'.format(self.row_pos), line.credit
        #                      and line.payment_id.name or '',
        #                      self.arial)
        #     memo = line.payment_id.communication or ''
        #     lang_2_name = line.payment_id.lang_2_name or ''
        #     description = ((memo + lang_2_name)
        #                    and "%s \\ %s" % (memo, lang_2_name)
        #                    or "%s \\ %s" % (line.name, line.lang_2_name))
        #     self.sheet.write('E{}'.format(self.row_pos), description,
        #                      self.arial)
        #     self.sheet.write('F{}'.format(self.row_pos),
        #                      line.debit,
        #                      self.arial)
        #     self.sheet.write('G{}'.format(self.row_pos),
        #                      line.credit,
        #                      self.arial)
        #     self.sheet.write_formula('H{}'.format(self.row_pos),
        #                              '=H{}+F{}-G{}'.format(
        #                                  self.row_pos-1, self.row_pos,
        #                                  self.row_pos), self.arial)
        #     self.sheet.write('I{}'.format(self.row_pos), '', self.arial)
        #     self.row_pos += 1
        # self.sheet.write('A{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('B{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('C{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('D{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('F{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('G{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('I{}'.format(self.row_pos), '',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write('E{}'.format(self.row_pos),
        #                  'Số dư cuối kỳ/ Ending balance',
        #                  self.arial_bold_center_border_no_top)
        # self.sheet.write_formula(
        #     'H{}'.format(self.row_pos), 'H{}'.format(self.row_pos-1),
        #     self.arial_bold_center_border_no_top)
        # self.row_pos += 1
        # self.sheet.write(
        #     'A{}'.format(self.row_pos),
        #     '- Sổ này có ... trang, đánh số từ trang 01 đến trang ...',
        #     self.bold_left)
        # self.row_pos += 1
        # self.sheet.write(
        #     'A{}'.format(self.row_pos), '- Ngày mở sổ: ...', self.bold_left)
        # self.row_pos += 1
        # self.sheet.write('H{}'.format(self.row_pos),
        #                  'Ngày..... tháng.... năm .......', self.bold_center)
        # self.row_pos += 1
        # self.sheet.write('A{}'.format(self.row_pos),
        #                  'Người ghi sổ\n(Ký, họ tên)', self.bold_center)
        # self.sheet.write('E{}'.format(self.row_pos),
        #                  'Kế toán trưởng\n(Ký, họ tên)', self.bold_center)
        # self.sheet.write('H{}'.format(self.row_pos),
        #                  'Giám đốc\n(Ký, họ tên, đóng dấu)', self.bold_center)
        #
        # for row in range(0, self.row_pos):
        #     self.sheet.set_row(row, 16)
        # self.sheet.set_row(1, 28)
        # self.sheet.set_row(11, 28)
        # self.sheet.set_row(self.row_pos-1, 28)

    def _define_format(self):

        self.normal_center = self.wb.add_format({
            'align': 'center',
            'valign': 'top',
            'font_name': 'Times New Roman',
        })
        self.normal_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'font_name': 'Times New Roman',
        })
        self.normal_center14 = self.wb.add_format({
            'align': 'center',
            'valign': 'top',
            'font_size': 14,
            'font_name': 'Times New Roman',
        })

        self.bold_center = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
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
            'font_name': 'Times New Roman',
        })
        self.bold_center14 = self.wb.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'top',
            'font_size': 14,
            'font_name': 'Times New Roman',
        })
        self.bold_left = self.wb.add_format({
            'bold': True,
            'align': 'left',
            'valign': 'top',
            'font_size': 12,
            'font_name': 'Times New Roman',
        })
        self.border_bot = self.wb.add_format({
            'bottom': 1,
        })
