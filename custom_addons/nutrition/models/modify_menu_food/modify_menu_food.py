from odoo import api, fields, models


class ModifyMenuFood(models.Model):
    _name = 'modify.menu.food'
    _description = 'Điều chỉnh thực đơn'

    standard_material_id = fields.Many2one('standard.material', 'Định mức dinh dưỡng')
    menu_food_id = fields.Many2one('menu.food', 'Tên thực đơn')
    is_breakfast = fields.Boolean('Thực đơn sáng')
    name = fields.Char('Tên thực đơn 2')
    appetizer = fields.Char('Khai vị')
    breakfast = fields.Char('Món sáng')
    soup = fields.Char('Canh')
    soup2 = fields.Char('Canh 2')
    meat = fields.Char('Mặn')
    meat2 = fields.Char('Mặn 2')
    after_lunch = fields.Char('Ăn xế')
    after_lunch2 = fields.Char('Ăn xế 2')
    fruit = fields.Char('Phụ trưa xế')
    fruit2 = fields.Char('Phụ trưa xế 2')
    total_student = fields.Integer('Sĩ số')
    price = fields.Float('Giá 1 phần')
    date_create = fields.Date('Ngày lập', default=fields.Date.today)
    line_ids = fields.One2many('modify.menu.food.line', 'modify_menu_food_id')
    amount_line_ids = fields.One2many('amount.modify.menu.line', 'modify_menu_food_id')
    standard_check = fields.Html(
        'Định mức dinh dưỡng chuẩn',
        compute='_compute_standard_check',
        help="Tính toán ra số lượng định mức so với chuẩn của bộ giáo dục đưa ra",
    )
    protein_cal = fields.Float('Hệ số đạm', default=4)
    limit_cal = fields.Float('Hệ số béo', default=9)
    gluco_cal = fields.Float('Hệ số đường', default=4)

    @api.depends('line_ids', 'amount_line_ids', 'standard_material_id')
    def _compute_standard_check(self):
        print("*" * 80)
        for rec in self:
            line_ids = rec.line_ids
            standard_id = rec.standard_material_id
            t_protein_a = t_protein_v = t_lipit_a = t_lipit_v = t_gluco = t_calo = t_amount = 0

            for line in line_ids:
                t_protein_a += line.protein_a
                t_protein_v += line.protein_v
                t_lipit_a += line.lipit_a
                t_lipit_v += line.lipit_v
                t_gluco += line.gluco
                t_calo += line.calo
                t_amount += line.amount
            total = """
                    <td> Tổng cộng</td>
                    <td> {t_protein_a}</td>
                    <td> {t_protein_v}</td>
                    <td> {t_lipit_a}</td>
                    <td> {t_lipit_v}</td>
                    <td> {t_gluco}</td>
                    <td> {t_calo}</td>
                    <td> {t_amount}</td>
                """.format(
                t_protein_a=t_protein_a,
                t_protein_v=t_protein_v,
                t_lipit_a=t_lipit_a,
                t_lipit_v=t_lipit_v,
                t_gluco=t_gluco,
                t_calo=t_calo,
                t_amount=t_amount
            )
            p_protein_a = 0 if standard_id.protein_a == 0 else t_protein_a / standard_id.protein_a
            p_protein_v = 0 if standard_id.protein_v == 0 else t_protein_v / standard_id.protein_v
            p_lipit_a = 0 if standard_id.lipit_a == 0 else t_lipit_a / standard_id.lipit_a
            p_lipit_v = 0 if standard_id.lipit_v == 0 else t_lipit_v / standard_id.lipit_v
            p_gluco = 0 if standard_id.gluco == 0 else t_gluco / standard_id.gluco
            p_calo = 0 if standard_id.calo == 0 else t_calo / standard_id.calo
            percent = """
                    <td> Tỷ lệ từng loại % </td>
                    <td> {p_protein_a}</td>
                    <td> {p_protein_v}</td>
                    <td> {p_lipit_a}</td>
                    <td> {p_lipit_v}</td>
                    <td> {p_gluco}</td>
                    <td> {p_calo}</td>
                """.format(
                p_protein_a=p_protein_a,
                p_protein_v=p_protein_v,
                p_lipit_a=p_lipit_a,
                p_lipit_v=p_lipit_v,
                p_gluco=p_gluco,
                p_calo=p_calo,
            )
            p_protein_a2 = 0 if (t_protein_a + t_protein_v) == 0 else \
                t_protein_a * 100 / (t_protein_a + t_protein_v)
            p_protein_v2 = 0 if (t_protein_a + t_protein_v) == 0 else \
                t_protein_v * 100 / (t_protein_a + t_protein_v)
            p_lipit_a2 = 0 if (t_lipit_a + t_lipit_v) == 0 else \
                t_lipit_a * 100 / (t_lipit_a + t_lipit_v)
            p_lipit_v2 = 0 if (t_lipit_a + t_lipit_v) == 0 else \
                t_lipit_v * 100 / (t_lipit_a + t_lipit_v)

            percent_av = """
                    <td> Động vật thực vật </td>
                    <td> {p_protein_a2}</td>
                    <td> {p_protein_v2}</td>
                    <td> {p_lipit_a2}</td>
                    <td> {p_lipit_v2}</td>
                    
                """.format(
                p_protein_a2=p_protein_a2,
                p_protein_v2=p_protein_v2,
                p_lipit_a2=p_lipit_a2,
                p_lipit_v2=p_lipit_v2
            )

            d_protein = (t_protein_a + t_protein_v)*100/(
                    standard_id.protein_a + standard_id.protein_v)
            d_lipit = (t_lipit_a + t_lipit_v) * 100 / (standard_id.lipit_a + standard_id.lipit_v)
            d_gluco = t_gluco*100/standard_id.gluco
            d_calo = t_calo*100/standard_id.calo

            rate_ok = """
                <td> Tỉ lệ đạt </td>
                <td> {d_protein}</td>
                <td> {d_lipit}</td>
                <td> {d_gluco}</td>
                <td> {d_calo}</td>
                    """.format(
                d_protein=d_protein,
                d_lipit=d_lipit,
                d_gluco=d_gluco,
                d_calo=d_calo
            )

            apply = """
                    <td> Định mức 1 ngày </td>
                    <td> 14.00</td>
                    <td> 26.00</td>
                    <td> 60.00 </td>
                """
            # p =
            PLG = """"""
            standard = """
                    <td> Định mức 1 ngày </td>
                    <td> {p_protein_a}</td>
                    <td> {p_protein_v}</td>
                    <td> {p_lipit_a}</td>
                    <td> {p_lipit_v}</td>
                    <td> {p_gluco}</td>
                    <td> {p_calo}</td>
                """.format(
                p_protein_a=standard_id.protein_a,
                p_protein_v=standard_id.protein_v,
                p_lipit_a=standard_id.lipit_a,
                p_lipit_v=standard_id.lipit_v,
                p_gluco=standard_id.gluco,
                p_calo=standard_id.calo,
            )


            content = """
                <div style="padding: 20px; font-family: Verdana, Geneva, sans-serif;">
                    <table style="background-color: #D2D2D2; height: 50px;
                    border-collapse: collapse; width: 100%;">
                        <tr>
                            <th style="width: 200px;">
                            <th style="width: 200px; " colspan="2">Đạm (g)</th>
                            <th style="width: 200px; " colspan="2">Béo (g)</th>
                            <th style="width: 100px; ">Đường (g)</th>
                            <th style="width: 100px; ">Calo (g)</th>
                            <th style="width: 120px; ">Tiền</th>
                        </tr>
                        <tr>
                            <th/>
                            <th style="width: 100px; ">Động vật (g)</th>
                            <th style="width: 100px; ">Thực vật (g)</th>
                            <th style="width: 100px; ">Động vật (g)</th>
                            <th style="width: 100px; ">Thực vật (g)</th>
                            <th/>
                            <th/>
                            <th/>
                        </tr>
                        <tr>
                            {total}
                        </tr>
                        <tr>
                            {standard}
                        </tr>
                        <tr>
                            {percent}
                        </tr>
                        <tr>
                            {percent_av}
                        </tr>
                        <tr>
                            {rate_ok}
                        </tr>
                        <tr>
                            {apply}
                        </tr>
                        <tr>
                            {PLG}
                        </tr>
                    </table>
                    <br/>
                </div>
                """.format(
                total=total,
                standard=standard,
                percent=percent,
                percent_av=percent_av,
                rate_ok=rate_ok,
                apply=apply,
                PLG=PLG
            )
            rec.standard_check = content
        return True


