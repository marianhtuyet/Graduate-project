import xlsxwriter
from odoo import models


class StudyclassReportXlsxTemplate(models.AbstractModel):
    _name = 'report.voucher_breakfast_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        self.company = self.env.user.company_id
        self.wb = workbook

        self.obj = objs
        self.sheet_name = 'Phiếu sáng'
        self.sheet = self.wb.add_worksheet(self.sheet_name)
        self._set_cells_size()
        self._define_format()
        for obj in objs:
            self.generate_template_header(obj)
            self.generate_content(obj)
            self.generate_footer(obj)

    def _set_cells_size(self):
        self.sheet.set_column('A:A', 14)
        self.sheet.set_column('B:B',33)
        self.sheet.set_column('C:E', 16)
        self.sheet.set_column('F:F', 18)
        self.row_pos = 2

    def generate_template_header(self, rec):
        self.xlsx_merge_range(
            'A{}:F{}'.format(self.row_pos, self.row_pos),
            'Đơn vị ....................',
            self.normal_left_14
        )

        self.row_pos += 1
        self.sheet.merge_range('A{}:F{}'.format(self.row_pos, self.row_pos),
                               'PHIẾU KÊ CHỢ SÁNG', self.bold_center_28)
        self.row_pos += 3
        self.xlsx_write(
            'D',
            'Số : {}'.format(rec.sequence),
            self.normal_left_14,
        )
        self.row_pos +=1
        self.sheet.merge_range('A{}:F{}'.format(self.row_pos, self.row_pos),
                               'Họ tên người nhận hàng : {}'.format(rec.name),
                               self.normal_left_14)
        self.row_pos += 1
        self.sheet.merge_range('A{}:F{}'.format(self.row_pos, self.row_pos),
                               'Địa chỉ( bộ phận): {}'.format(rec.street),
                               self.normal_left_14)
        self.row_pos += 1
        self.sheet.merge_range('A{}:F{}'.format(self.row_pos, self.row_pos),
                               'Số trẻ: {}'.format(rec.total_student),
                               self.normal_left_14)
        self.row_pos += 1
        self.sheet.merge_range('A{}:F{}'.format(self.row_pos, self.row_pos),
                               'Điểm tâm: {}'.format(rec.name_food),
                               self.normal_left_14)

    def generate_content(self, rec):
        self.row_pos += 1
        self.xlsx_write('A', 'STT', self.bold_center14)
        self.xlsx_write('B', 'TÊN, NHÃN HIỆU', self.bold_center14)
        self.xlsx_write('C', 'Đơn vị tính', self.bold_center14)
        self.xlsx_write('D', 'Số lượng', self.bold_center14)
        self.xlsx_write('E', 'Đơn giá', self.bold_center14)
        self.xlsx_write('F', 'Thành Tiền', self.bold_center14)
        self.row_pos += 1
        count_line = 0
        for line in rec.line_ids:
            count_line += 1
            self.xlsx_write('A', count_line, self.border_center_14)
            self.xlsx_write('B', line.nutrition_id.name, self.border_left_14)
            self.xlsx_write('C', line.uom_id.name, self.border_center_14)
            self.xlsx_write('D', '{:,.0f}'.format(line.quantity), self.border_center_14)
            self.xlsx_write('E', '{:,.0f}'.format(line.price), self.border_center_14)
            self.xlsx_write('F', '{:,.0f}'.format(line.amount), self.border_center_14)
            self.row_pos += 1

    def generate_footer(self, rec):
        self.xlsx_write('A', 'Tổng cộng', self.bold_center14)
        self.xlsx_write('B', '', self.bold_center14)
        self.xlsx_write('C', '', self.bold_center14)
        self.xlsx_write('D', '', self.bold_center14)
        self.xlsx_write('E', '', self.bold_center14)
        self.xlsx_write('F', '{:,.0f}'.format(rec.total_amount), self.bold_center14)
        self.row_pos += 3
        self.xlsx_merge_range(
            'A{}:F{}'.format(self.row_pos, self.row_pos),
            rec.total_2_text,
            self.normal_left_14
        )
        self.row_pos += 1
        self.xlsx_merge_range(
            'E{}:F{}'.format(self.row_pos, self.row_pos),
            'Ngày ' + str(self.date_format(rec.date_create)),
            self.normal_left_14
        )
        self.row_pos += 1
        self.xlsx_write('C', 'NGƯỜI NHẬN', self.bold_center14)
        self.xlsx_write('E', 'NGƯỜI GIAO', self.bold_center14)
        self.xlsx_write('F', 'NGƯỜI LẬP PHIẾU', self.bold_center14)
        self.row_pos += 1
        self.xlsx_write('C', rec.receiver, self.bold_center14)
        self.xlsx_write('E', rec.transfer_user, self.bold_center14)
        self.xlsx_write('F', rec.create_user, self.bold_center14)


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
        self.normal_left_14 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 14,
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
        self.normal_right_14 = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 14,
            'text_wrap': True,
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
            'border': 1,
            'font_name': 'Times New Roman',
        })
        self.bold_center_28 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 28,
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
        self.border_center_14 = self.wb.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 14,
            'font_name': 'Times New Roman',
        })
        self.border_left_14 = self.wb.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'font_size': 14,
            'font_name': 'Times New Roman',
        })
