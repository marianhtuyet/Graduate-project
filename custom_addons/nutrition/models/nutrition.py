from odoo import api, fields, models


class Nutrition(models.Model):
    _name = 'nutrition'

    product_id = fields.Many2one('product.template', 'Sản phẩm', ondelete="cascade",
                              required=True, delegate=True)
    # Inherit các trường của product mà không lấy view của product
    # name = fields.Char('Tên thực phẩm', required=True)
    constant = fields.Float('Hệ số thai bo')
    protein = fields.Float('Đạm')
    lipit = fields.Float('Béo')
    gluco = fields.Float('Đường')
    calo = fields.Float()
    photpho = fields.Float('P')
    fe = fields.Float('Fe')
    caroten = fields.Float('Caroten')
    b1 = fields.Float('B1')
    b2 = fields.Float('B2')
    pp = fields.Float('PP')
    cacbon = fields.Float('C')
    cholesterol = fields.Float('Cholesterol')
    is_vegetable = fields.Boolean('Rau quả')
    is_animal = fields.Boolean('Động vật')
    is_fruit = fields.Boolean('Thực vật')
    transfer_gam  = fields.Float('Quy đổi gam')

    # MaNhaCungCap
    packaging_id = fields.Many2one('packaging', 'Bao bì')
    type_food = fields.Many2one('type.food', 'Loại thức ăn')
    # uom_id = fields.Many2one(
    #     'uom.uom',
    #     string='Đơn vị tính')
