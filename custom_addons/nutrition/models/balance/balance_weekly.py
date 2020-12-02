from datetime import timedelta, date, datetime
from itertools import chain

from odoo import api, fields, models
import random
import logging
import unidecode
from deap import base
from deap import creator
from deap import tools
# models.TransientModel


# Configuration
# Assuming that there are 4 timeslots per day
# and 5 days on which you can have an exam
timeslots_per_day = 10
DAYS = 5

# Genetic algorithm variables
POPULATION_COUNT = 1000
GENERATIONS_NUMBER = 100
CROSSOVER_PROBABILITY = 0.2
MUTATION_PROBABILITY = 0.1
MUTATION_CHANGE_EXAM_PROBABILITY = 0.1

available_timeslots = DAYS * timeslots_per_day

# punishments weights
STUDENT_TAKING_TWO_EXAMS_AT_ONCE = 500
STUDENT_TAKING_MORE_THAN_TWO_EXAMS_IN_ONE_DAY = 10
STUDENT_TAKING_EXAMS_ONE_AFTER_ANOTHER = 5
STUDENT_TAKING_TWO_EXAMS_IN_ONE_DAY = 4
meal_not_right = 1000
meal_enough_nutrition = 10000
meal1 =5
daily_meal = [_ for _ in range(10)]
# Maps year to list of students (each student is represented as a list of exams)
students_exams = {
    1: [daily_meal[:] for _ in range(meal1)],
}


class MenuAutomaticWeekly(models.Model):
    _name = 'menu.automatic.weekly'
    _description = 'Thực đơn tự động tuần'

    date_start = fields.Date(required=True, default=date.today() + timedelta(days=-date.today().weekday()))
    date_end = fields.Date(compute='_compute_date_end')
    name = fields.Char(compute='_compute_name')
    line_ids = fields.One2many('menu.automatic.weekly.line', 'menu_automatic_weekly_id')
    line_nutrition_ids = fields.One2many('meal.food.line', 'menu_automatic_id')

    def timeslot_to_day(self, timeslot):
        return int(timeslot / timeslots_per_day)

    def timeslot_to_dayslot(self, timeslot):
        return timeslot % timeslots_per_day

    def check_ind(self, ind):
        count_error = 0
        for i in range(5):
            for index, item in enumerate(ind):
                if index % 10 == 0 or index % 10 == 5:
                    if item > 15 or item < 0:
                        count_error += 1
                if index % 10 == 1 or index % 10 == 6:
                    if item > 21 or item < 16:
                        count_error += 1
                if index % 10 == 2 or index % 10 == 7:
                    if item > 42 or item < 22:
                        count_error += 1
                if index % 10 == 3 or index % 10 == 8:
                    if item > 62 or item < 43:
                        count_error += 1
                if index % 10 == 4 or index % 10 == 9:
                    if item > 81 or item < 63:
                        count_error += 1
        return count_error
    # The individual is a list of numbers
    # Item position in the list is index of exam in `exams` list
    # Item value is the starting time of exam



    def evaluate(self, individual, inverse=True):
        """
        :param individual: List of numbers (timeslots) for exams (the position of number is the exam number.
        :param inverse: Whether we return inverse of punishments or punishment and is_valid values.
        The `inverse=False` is used for debugging/finding best parameters.
        """
        punishments = 0
        two_exams_at_once = 0
        exam_after_another = 0
        more_than_two_exams_at_one_day = 0
        two_exams_at_one_day = 0
        count = 0

        count_error = self.check_ind(individual)
        if count_error > 0:
            punishments += count_error * meal_not_right
        # Iterate over students from all years
        for student_exams in chain(*students_exams.values()):
            student_timeslots = [individual[exam] for exam in student_exams]
            student_timeslots.sort()

            # number of exams on particular day
            exams_per_day = [0] * 10

            prev_timeslot = student_timeslots[0]
            prev_day = self.timeslot_to_day(prev_timeslot)
            # số ngày / số lần kiểm tra.
            exams_per_day[prev_day] += 1
            # Qua vòng lặp để tính các môn trùng lắp trong cùng một ngày
            for timeslot in student_timeslots[1:]:
                diff = timeslot - prev_timeslot
                day = self.timeslot_to_day(timeslot)

                if prev_day == day:
                    if diff == 0:
                        two_exams_at_once += 1
                    elif diff == 1:
                        exam_after_another += 1

                exams_per_day[day] += 1
                prev_timeslot = timeslot
                prev_day = day

            # Tìm các ngày có 2 môn học trở lên để trừ điểm đánh giá
            for exams_count in exams_per_day:
                if exams_count > 2:
                    more_than_two_exams_at_one_day += 1
                elif exams_count == 2:
                    two_exams_at_one_day += 1
        # dựa vào các biến, tính điểm cho invidual đó.
        punishments += two_exams_at_once * STUDENT_TAKING_TWO_EXAMS_AT_ONCE
        punishments += exam_after_another * STUDENT_TAKING_EXAMS_ONE_AFTER_ANOTHER
        punishments += more_than_two_exams_at_one_day * STUDENT_TAKING_MORE_THAN_TWO_EXAMS_IN_ONE_DAY
        punishments += two_exams_at_one_day * STUDENT_TAKING_TWO_EXAMS_IN_ONE_DAY
        if inverse:
            return 1.0 / (1.0 + punishments),
        else:
            is_valid = two_exams_at_once == 0
        meals = self.env['meal.food'].search([])
        fixed_meal = meals.filtered(lambda m: ('Cố định') in m.name)
        list_meals = []
        list_meal_food_line_ids = []
        for i in range(5):
            list_meals.append(meals[individual[0 + i * 10]])
            list_meals.append(meals[individual[5 + i * 10]])
            list_meals.append(meals[individual[3 + i * 10]])
            list_meals.append(meals[individual[2 + i * 10]])
            list_meals.append(meals[individual[7 + i * 10]])
            list_meals.append(meals[individual[4 + i * 10]])
            list_meals.append(meals[individual[1 + i * 10]])
            list_meals.append(meals[individual[6 + i * 10]])


        for line in list_meals:
            for nutrition in line.line_ids:
                list_meal_food_line_ids.append(nutrition)
        #Thêm các gia vị cố định
        for i in range(5):
            for line in fixed_meal.line_ids:
                list_meal_food_line_ids.append(line)
        p, l, g = self._compute_standard_check(list_meal_food_line_ids)

        if p > 12 and p < 20 and 30 > l > 23 and 65 > g > 60:
            logging.info("2"*100)
            punishments -= meal_enough_nutrition
        else:
            punishments += meal_enough_nutrition
        return punishments, is_valid, {
            "two exams at once": two_exams_at_once,
            "exam after another": exam_after_another,
            "more than two exams at one day": more_than_two_exams_at_one_day,
            "two exams at one day": two_exams_at_one_day
        }

    @api.depends('date_start')
    def _compute_date_end(self):
        for rec in self:
            rec.date_end = rec.date_start + timedelta(days=-rec.date_start.weekday() + 4)

    @api.onchange('date_start', 'date_end')
    def onchange_date_start(self):
        for rec in self:
            rec.date_end = rec.date_start + timedelta(days=-rec.date_start.weekday() + 4)
            rec.name = '{} - {}'.format(
                datetime.strptime(rec.date_start, "%Y-%m-%d"),
                datetime.strptime(rec.date_end, "%Y-%m-%d")
            )

    @api.depends('date_start', 'date_end')
    def _compute_name(self):
        for rec in self:
            rec.name = '{} - {}'.format(
                rec.date_start.strftime("%Y-%m-%d"),
                rec.date_end.strftime("%Y-%m-%d"),
            )

    def create_menu_automatic(self):
        meals = self.env['meal.food'].search([])
        breakfast = meals.filtered(lambda m: m.is_breakfast == 1)
        brunch = meals.filtered(lambda m: m.is_brunch == 1)
        soup = meals.filtered(lambda m: m.is_soup == 1)
        main_meal = meals.filtered(lambda m: m.is_main_lunch == 1)
        fruit = meals.filtered(lambda m: m.is_lunch == 1)
        total_meals = breakfast + brunch + soup + main_meal + fruit
        meals1_indexes = list(range(len(breakfast)))
        last_index = meals1_indexes[-1]
        meals2_indexes = list(range(last_index + 1, last_index + 1 + len(brunch)))
        last_index = meals2_indexes[-1]
        meals3_indexes = list(range(last_index + 1, last_index + 1 + len(soup)))
        last_index = meals3_indexes[-1]
        meals4_indexes = list(range(last_index + 1, last_index + 1 + len(main_meal)))
        last_index = meals4_indexes[-1]
        meals5_indexes = list(range(last_index + 1, last_index + 1 + len(fruit)))

        self.ga(pop_count=POPULATION_COUNT,
                generations_number=GENERATIONS_NUMBER,
                cx_prob=CROSSOVER_PROBABILITY,
                mut_prob=MUTATION_PROBABILITY,
                mut_change_exam_prob=MUTATION_CHANGE_EXAM_PROBABILITY,
                evaluate_func=self.evaluate,  # hàm đánh giá
                available_timeslots=available_timeslots,
                exams=total_meals,
                timeslot_to_day=self.timeslot_to_day,
                timeslot_to_dayslot=self.timeslot_to_dayslot,
                print_best=True,
                meals1_indexes=meals1_indexes,
                meals2_indexes=meals2_indexes,
                meals3_indexes=meals3_indexes,
                meals4_indexes=meals4_indexes,
                meals5_indexes=meals5_indexes,
                meals=total_meals
                )

    def ga(self, pop_count, generations_number,
           cx_prob, mut_prob, mut_change_exam_prob,
           evaluate_func, available_timeslots, exams,
           timeslot_to_day, timeslot_to_dayslot,
           print_best, select_method=None,
           meals1_indexes=None, meals2_indexes=None,
           meals3_indexes=None, meals4_indexes=None
           , meals5_indexes=None, meals=None
           ):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        # base.Fitness is a type of deap.
        logging.info('creator.FitnessMax: {}'.format(creator.FitnessMax))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("random_timeslot", random.randint, 0, max(meals1_indexes))
        toolbox.register("random_timeslot2", random.randint, max(meals1_indexes) + 1, max(meals2_indexes))
        toolbox.register("random_timeslot3", random.randint, max(meals2_indexes) + 1, max(meals3_indexes))
        toolbox.register("random_timeslot4", random.randint, max(meals3_indexes) + 1, max(meals4_indexes))
        toolbox.register("random_timeslot5", random.randint, max(meals4_indexes) + 1, max(meals5_indexes))

        # truyền biến vào hàm random_timeslot trong random_timeslot gọi hàm random.randint(), 2 biến 0 và (available_timeslots-1)
        # hàm này dùng để xác định khoảng giá trị để random
        toolbox.register("individual", tools.initCycle,
                         creator.Individual, [
                             toolbox.random_timeslot,
                             toolbox.random_timeslot2,
                             toolbox.random_timeslot3,
                             toolbox.random_timeslot4,
                             toolbox.random_timeslot5,
                         ],
                         n=10)

        a = toolbox.individual()

        # Tạo hàm individual, trong đó gọi hàm random_timeslot rồi lưu vào creator.individual, chạy hàm n lần
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        # lưu kết qquả của hàm individual ở trên vào trong population của toolbox.

        # mate/crossover function: ghép đôi và tiến hoá
        toolbox.register("mate", tools.cxOnePoint)
        # tạo ra tuple của 2 thằng ngẫu nhiên. sử dụng random int của python
        logging.info('available_timeslots:  {}'.format(available_timeslots))
        logging.info('mut_change_exam_prob:  {}'.format(mut_change_exam_prob))
        toolbox.register("mutate", tools.mutUniformInt, low=0, up=available_timeslots - 1, indpb=mut_change_exam_prob)

        toolbox.register("evaluate", evaluate_func)
        # gọi hàm evaluate_func

        if select_method:
            select_func, select_kwargs = select_method
        else:
            select_func, select_kwargs = tools.selTournament, {'tournsize': 3}

        toolbox.register("select", select_func, **select_kwargs)

        pop = toolbox.population(n=pop_count)

        # chọn ngẫu nhiên 100 cá thể
        # tập hợp mẫu tạo ra để chọn các cá thể, trong naỳ có 50 phần tử, mỗi phần tử có len=14.
        best_ever = pop[0]
        # Calculate fitness for first generation, chọn ra 100 cá thể, lấy cá thể tốt nhất
        for ind in pop:
            ind.fitness.values = toolbox.evaluate(ind)
            if ind.fitness.values > best_ever.fitness.values:
                best_ever = toolbox.clone(ind)
        # Lai ghép 50 thế hệ
        logging.info("Algorithm start")

        for gen in range(generations_number):
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            # (nhân bản, set offspring = với pop, lấy 100 phần tử từ pop
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                # offspring[::2] : lấy ra các phần tử ở vị trí chẵn 0, 2, 4, 6,...
                # offspring[1::2]: lấy ra các phần tử ở vj trí lẻ 1, 3, 5, 7,...
                a = random.random()
                if a < cx_prob:  # cx_prob = 0.2
                    toolbox.mate(child1, child2)
                    # del dùng để xoá phần tử trong list
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offspring
            for mutant in offspring:
                self.check_ind(mutant)
                if random.random() < mut_prob:  # mut_prob = 0.1 cái này dùng để giới hạn lại số lần đột biến
                    logging.info('mutant:  {}'.format( mutant))
                    toolbox.mutate(mutant)
                    up = available_timeslots - 1
                    indpb = mut_change_exam_prob
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            # tìm những cá thể không có fitness, là những cá thể đã biến đổi trước đó (lai hoặc đột biến)
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            # tính fitness cho các cá thể đó lưu lại thành 1 danh sách
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                # gán tương ứng các giá trị fitness đã được tính thành chỉ
                # số fitness của cá thể tìm ra trong invalid_ind

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            current_best = tools.selBest(pop, k=1)[0]
            if current_best.fitness.values > best_ever.fitness.values:
                best_ever = toolbox.clone(ind)
        logging.info("Algorithm end")

        # Printing result
        def print_individual(ind):
            logging.info("Printing individual")
            logging.info("Raw:{}".format(ind))
            logging.info("Fitness:{}".format( ind.fitness.values))
            logging.info(toolbox.evaluate(ind, inverse=False))
            logging.info('meals:  {}'.format( meals))
            type_food = ''
            for index in ind:

                if meals[index].is_breakfast == 1:
                    type_food = 'Sáng: '
                if meals[index].is_brunch == 1:
                    type_food = 'Xế: '
                if meals[index].is_soup == 1:
                    type_food = 'Canh : '
                if meals[index].is_main_lunch == 1:
                    type_food = 'Mặn: '
                if meals[index].is_lunch == 1:
                    type_food = 'Tráng miệng: '
                print('Stt: {} Món ăn:  {}  {}'.format(index, type_food, meals[index].name))

        if print_best:
            print_individual(best_ever)

        detail = self.create({
            'date_start': date.today() + timedelta(days= -date.today().weekday()),
            'date_end': date.today() + timedelta(days= -date.today().weekday() + 4),
        })

        menu_line_env = self.env['menu.automatic.weekly.line']
        menu_food_line = self.env['meal.food.line']
        list_meals = []
        for i in range(5):
            line_weekly = menu_line_env.create({
                'menu_automatic_weekly_id': detail.id,
                'day_in_week': i + 2,
                'breakfast1': meals[best_ever[0 + i*10]].id ,
                'breakfast2': meals[best_ever[5 + i*10]].id,
                'main_lunch': meals[best_ever[3 + i*10]].id,
                'soup1': meals[best_ever[2 + i*10]].id,
                'soup2': meals[best_ever[7 + i*10]].id,
                'lunch': meals[best_ever[4 + i*10]].id,
                'tea1': meals[best_ever[1 + i*10]].id,
                'tea2': meals[best_ever[6 + i*10]].id,
            })
            list_meals.append(meals[best_ever[0 + i*10]])
            list_meals.append(meals[best_ever[5 + i * 10]])
            list_meals.append(meals[best_ever[3 + i * 10]])
            list_meals.append(meals[best_ever[2 + i * 10]])
            list_meals.append(meals[best_ever[7 + i * 10]])
            list_meals.append(meals[best_ever[4 + i * 10]])
            list_meals.append(meals[best_ever[1 + i * 10]])
            list_meals.append(meals[best_ever[6 + i * 10]])
        for line in list_meals:
            for nutrition in line.line_ids:
                temp = menu_food_line.create({
                    'nutrition_id': nutrition.nutrition_id.id,
                    'quantity' : nutrition.quantity,
                    'protein_a': nutrition.protein_a,
                    'protein_v': nutrition.protein_v,
                    'lipit_a': nutrition.lipit_a,
                    'lipit_v': nutrition.lipit_v,
                    'gluco': nutrition.gluco,
                    'calo': nutrition.calo,
                    'menu_automatic_id': detail.id
                })
        return best_ever.fitness.values[0]


    def _compute_standard_check(self, rec):
        line_ids = rec
        t_protein_a = t_protein_v = t_lipit_a = t_lipit_v = t_gluco = t_calo  = 0
        protein_cal = self.env['ir.config_parameter'].sudo().get_param('nutrition_protein')
        lipit_cal = self.env['ir.config_parameter'].sudo().get_param('nutrition_lipit')
        gluco_cal = self.env['ir.config_parameter'].sudo().get_param('nutrition_gluco')
        for line in line_ids:
            t_protein_a += line.protein_a
            t_protein_v += line.protein_v
            t_lipit_a += line.lipit_a
            t_lipit_v += line.lipit_v
            t_gluco += line.gluco
            t_calo += line.calo

        total_p = (t_protein_v + t_protein_a) * float(protein_cal)
        total_l = (t_lipit_v + t_lipit_a) * float(lipit_cal)
        total_g = t_gluco * float(gluco_cal)
        total_calo = total_p + total_l + total_g
        p = l = g = 0
        if total_calo != 0:
            p = total_p * 100 / total_calo
            l = total_l * 100 / total_calo
            g = total_g * 100 / total_calo
        logging.info("*"*80)
        logging.info('total_p, total_l, total_g, total_calo:  {} {} {} {}'.format(total_p, total_l, total_g, total_calo))
        logging.info('p: {}'.format(p))
        logging.info('l: {}'.format(l))
        logging.info('g: {}'.format(g))
        return p,l,g

    @api.multi
    def create_new_automatic_menu(self):
        new_menu = self.create_menu_automatic()
        automatic_menu = self.env['menu.automatic.weekly'].search([], order='create_date desc', limit=1)
        view_id = self.env.ref('nutrition.menu_automatic_weekly_view').id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Translation',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
            'res_model': self._name,
            'res_id': automatic_menu.id,
            'view_id': view_id,
        }
