from odoo import models

DEFAULT_FONT = 'times new roman'

class NutritionReportXlsxTemplate(models.AbstractModel):
    _name = 'report.nutrition.nutrition_balance_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        self.company = self.env.user.company_id
        self.date_from = objs.date_from
        self.date_to = objs.date_to

        self.wb = workbook
        self.obj = objs[0]
        self.sheet_name = 'Balance'
        self.sheet = self.wb.add_worksheet(self.sheet_name)
        self._set_cells_size()
        self._define_format()
        self.generate_template_header()
        # self.generate_template_content()

    def _set_cells_size(self):
        self.sheet.set_column('A:B', 13)
        self.sheet.set_column('C:D', 11)
        self.sheet.set_column('E:E', 28)
        self.sheet.set_column('F:G', 13)
        self.sheet.set_column('I:I', 13)
        self.sheet.set_column('H:H', 17)
        self.row_pos = 1

    def generate_template_header(self):
        self.sheet.write('A{}'.format(self.row_pos),
                         'Đơn vị: ',
                         self.normal_left_10)

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
