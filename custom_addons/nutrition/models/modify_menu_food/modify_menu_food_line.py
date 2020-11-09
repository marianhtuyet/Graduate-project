from odoo import api, fields, models


class ModifyMenuFoodLine(models.Model):
    _name = 'modify.menu.food.line'
    _description = 'Chi tiết điều chỉnh thực đơn'

    modify_menu_food_id = fields.Many2one('modify.menu.food')
    nutrition_id = fields.Many2one('nutrition')
    quantity = fields.Float('Lượng khẩu phần đơn vị tính')
    qty_g = fields.Float('Lượng 1 trẻ', compute='_compute_balance_nutrition', store=True,)
    price = fields.Float('Đơn giá')
    protein_a = fields.Float(
        'Đạm động vật',
        compute='_compute_balance_nutrition',
        store=True,
    )
    protein_v = fields.Float(
        'Đạm thực vật vật',
        compute='_compute_balance_nutrition',
        store=True,
    )
    lipit_a = fields.Float('Béo động vật', compute='_compute_balance_nutrition', store=True,)
    lipit_v = fields.Float('Béo thực vật', compute='_compute_balance_nutrition', store=True,)
    gluco = fields.Float('Đường', compute='_compute_balance_nutrition', store=True,)
    calo = fields.Float(compute='_compute_balance_nutrition', store=True,)
    amount = fields.Float(
        'Tiền vnđ',
        help='Tiền trên 1 học sinh',
        compute='_compute_balance_nutrition',
        store=True,
    )
    qty_eat = fields.Float(
        'Thực ăn một nhóm',
        compute='_compute_balance_nutrition',
        store=True,
    )
    constant = fields.Float(
        'Hệ số thải bỏ',
        compute='_compute_balance_nutrition',
        store=True,
    )
    qty_buy = fields.Float(
        'Thực mua một nhóm',
        compute='_compute_balance_nutrition',
        store=True
    )
    # uom_id = fields.Many2one(
    #     'uom.uom',
    #     string='Đơn vị tính',
    #     related=nutrition_id.uom_id
    # )
    qty_uom = fields.Float(
        'Lượng 1 trẻ theo đơn vị tính',
        compute='_compute_balance_nutrition',
        digits=(32,12),
        store=True,
    )

    @api.depends('nutrition_id', 'nutrition_id.gluco', 'modify_menu_food_id',
                 'modify_menu_food_id.menu_food_id', 'modify_menu_food_id.amount_line_ids',
                 'modify_menu_food_id.total_student')
    def _compute_balance_nutrition(self):
        print("*"*80)
        print(len(self))
        for record in self:
            line_ids = record.modify_menu_food_id.line_ids
            for rec in line_ids:
                amount_ids = rec.modify_menu_food_id.amount_line_ids
                total_student = rec.modify_menu_food_id.total_student
                qty_buy = qty_eat = 0
                nutrition_id = rec.nutrition_id

                for line in amount_ids:
                    if line.nutrition_id.name == rec.nutrition_id.name:
                       qty_buy = line.quantity
                rec.constant = rec.nutrition_id.constant
                rec.qty_eat = qty_eat =  qty_buy * (1- rec.constant/100)
                rec.qty_buy = qty_buy
                rec.qty_g = 0 if total_student == 0 else qty_eat * 1000 / total_student
                rec.qty_uom = 0 if total_student == 0 else qty_eat / total_student
                rec.amount = 0 if total_student == 0 else qty_buy * rec.price / total_student
                print('-'*80)
                print('rec: ', rec)
                print('total_student, qty_buy, nutrition_id', total_student, qty_buy, nutrition_id)
                print('rec.qty_eat, rec.qty_buy,  rec.qty_g , rec.qty_uom, rec.amount',
                      rec.qty_eat, rec.qty_buy,  rec.qty_g , rec.qty_uom, rec.amount)
                if nutrition_id:
                    if nutrition_id.is_fruit:
                        rec.protein_v = 0 if total_student == 0 else \
                            nutrition_id.protein * qty_eat / total_student
                        rec.lipit_v = 0 if total_student == 0 else nutrition_id.lipit* qty_eat / total_student
                    elif rec.nutrition_id.is_animal:
                        rec.protein_a = 0 if total_student == 0 else nutrition_id.protein* qty_eat / total_student
                        rec.lipit_a = 0 if total_student == 0 else nutrition_id.lipit* qty_eat / total_student
                    rec.gluco = 0 if total_student == 0 else nutrition_id.gluco* qty_eat / total_student
                    rec.calo = 0 if total_student == 0 else nutrition_id.calo* qty_eat / total_student
        return True
