from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)

DEFAULT_FONT = 'times new roman'
BG_COLOR = '#7ED1C3'

class ReportXlsxAbstract(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'

    def setup_sheet(self, sheet_name):
        self.sheet_name = sheet_name
        self.sheet = self.wb.add_worksheet(self.sheet_name)
        self.sheet.set_margins(0.2, 0.3, 0.35, 0.15)
        self.sheet.center_horizontally()
        self.sheet.set_paper(9)  # 9: A4 paper format
        self.sheet.set_footer("Page &P of &N")

    def convert_col_num_to_letter(self, col_num):
        col_num += 1  # we convert the column of 0 to 1
        col_text = ""
        while col_num > 0:
            col_num, remainder = divmod(col_num - 1, 26)
            col_text = chr(65 + remainder) + col_text
        return col_text

    def _define_format(self):
        # {normal|bold|italic|bold-italic}_{left|center|right}_{size: 9..14}
        # _{optional: vbottom for vertical align bottom, default center}
        # _{optional: border}

        # Normal
        self.normal_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_left_11 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.normal_left_12 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })
        self.normal_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_center_10 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_center_11 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        self.normal_center_12 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })

        self.normal_right_10 = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_right_11 = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        # # Normal with options
        self.normal_left_10_border = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_left_11_border = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        self.normal_right_11_border = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.normal_right_12_border = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })

        self.normal_center_9_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 9,
            'font_name': DEFAULT_FONT,
        })
        self.normal_center_10_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.normal_center_11_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        # Bold
        self.bold_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.bold_left_11 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.bold_left_12 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })
        self.bold_left_13 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 13,
            'font_name': DEFAULT_FONT,
        })

        self.bold_center_9 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 9,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_10 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_11 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_12 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })

        self.bold_center_13 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 13,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_14 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 14,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_28 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 28,
            'font_name': DEFAULT_FONT,
        })

        self.bold_right_11 = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        # # Bold with options
        self.bold_left_12_border = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'border': 1,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })

        self.bold_center_9_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'border': 1,
            'font_size': 9,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_11_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'border': 1,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.bold_center_13_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'border': 1,
            'font_size': 13,
            'font_name': DEFAULT_FONT,
        })

        # Italic
        self.italic_left_10 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })
        self.italic_left_11 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })
        self.italic_left_14 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 14,
            'font_name': DEFAULT_FONT,
        })

        self.italic_center_9 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 9,
            'font_name': DEFAULT_FONT,
        })
        self.italic_center_10 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })

        self.italic_center_11 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        # # Italic with options
        self.italic_center_10_border = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
            'border': 1,
        })
        self.italic_center_10_border_text_wrap = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'italic': True,
            'font_size': 10,
            'font_name': DEFAULT_FONT,
            'border': 1,
            'text_wrap': True,
        })

        # Bold Italic
        self.bold_italic_left_12 = self.wb.add_format({
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'italic': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
        })

        self.bold_italic_center_14 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'italic': True,
            'font_size': 14,
            'font_name': DEFAULT_FONT,
        })

        # OTHER
        self.border_bot = self.wb.add_format({
            'bottom': 1,
        })
        self.num_digital_11_border = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00',
            'border': 1,
            'font_size': 11,
            'font_name': DEFAULT_FONT,
        })

        self.num_digital_10_wo_decimal_border = self.wb.add_format({
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0',
            'font_size': 10,
            'font_name': DEFAULT_FONT,
        })

        self.red_bold_center_14 = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_color': 'red',
            'font_size': 14,
            'font_name': DEFAULT_FONT,
        })
        self.underline_italic_bold_13 = self.wb.add_format({
            'underline': True,
            'italic': True,
            'bold': True,
            'font_size': 13,
            'font_name': DEFAULT_FONT,
        })
        self.normal_center_9_text_wrap = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 9,
            'font_name': DEFAULT_FONT,
            'text_wrap': True,
        })
        self.bold_center_12_bg = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
            'bg_color': BG_COLOR,
            'border': 1,
            'text_wrap': True,
        })

        self.normal_center_12_bg = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
            'bg_color': BG_COLOR,
            'border': 1,
            'text_wrap': True,
        })
        self.bold_center_12_rotate = self.wb.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 12,
            'font_name': DEFAULT_FONT,
            'bg_color': BG_COLOR,
            'border': 1,
            'text_wrap': True,
            'rotation': -90,
        })

    def xlsx_write_merge_center(self, cell1, cell2, value):
        cell1, cell2 = list(cell1), list(cell2)
        cell1[1], cell2[1] = str(cell1[1]), str(cell2[1])
        self.sheet.merge_range('{}:{}'.format(''.join(cell1), ''.join(cell2)),
                               value, self.bold_center_9_border)

    def xlsx_merge_range(self, range_cells, text, style):
        self.sheet.merge_range(range_cells, text, style)

    def xlsx_write_header(self, column, text):
        self.xlsx_write(column, text, self.bold_center_10)

    def xlsx_write_center(self, cell, value):
        self.sheet.write(cell, value, self.bold_center_9_border)

    def xlsx_write(self, column, text, style):
        self.sheet.write(
            '{}{}'.format(column, self.row_pos),
            text,
            style,
        )

    def xlsx_write_text(self, column, text):
        self.xlsx_write(
            column,
            text or '',
            self.normal_left_10,
        )

    def xlsx_write_date(self, column, my_date):
        self.xlsx_write(
            column,
            my_date and self.date_format(my_date) or '',
            self.normal_center_10,
        )

    def xlsx_write_number(self, column, text):
        self.xlsx_write(
            column,
            text or '',
            self.normal_right_10,
        )

    def date_format(self, my_date):
        return fields.Date.to_string(my_date)
