from datetime import timedelta, date, datetime
from itertools import chain

from odoo import api, fields, models
import random

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
POPULATION_COUNT = 100
GENERATIONS_NUMBER = 50
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
meal1 =5
daily_meal = [_ for _ in range(10)]
# Maps year to list of students (each student is represented as a list of exams)
students_exams = {
    1: [daily_meal[:] for _ in range(meal1)],
}


class MenuAutomaticWeekly(models.Model):
    _name = 'menu.automatic.weekly'
    _description = 'Thực đơn tự động tuần'

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


    date_start = fields.Date(required=True, default= date.today() + timedelta(days= -date.today().weekday()))
    date_end = fields.Date(compute='_compute_date_end')
    name = fields.Char(compute='_compute_name')
    line_ids = fields.One2many('menu.automatic.weekly.line', 'menu_automatic_weekly_id')

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
                datetime.strptime(rec.date_start, "%Y-%m-%d"),
                datetime.strptime(rec.date_end, "%Y-%m-%d")
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
        print('creator.FitnessMax: ', creator.FitnessMax)
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()
        toolbox.register("random_timeslot", random.randint, 0, max(meals1_indexes))
        toolbox.register("random_timeslot2", random.randint, max(meals1_indexes) + 1, max(meals2_indexes))
        toolbox.register("random_timeslot3", random.randint, max(meals2_indexes) + 1, max(meals3_indexes))
        toolbox.register("random_timeslot4", random.randint, max(meals3_indexes) + 1, max(meals4_indexes))
        toolbox.register("random_timeslot5", random.randint, max(meals4_indexes) + 1, max(meals5_indexes))

        print('max(meals1_indexes):  ', max(meals1_indexes))
        print('max(meals2_indexes):  ', max(meals2_indexes))
        print('max(meals3_indexes):  ', max(meals3_indexes))
        print('max(meal4_indexes):  ', max(meals4_indexes))
        print('max(meal5_indexes):  ', max(meals5_indexes))
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
        print('available_timeslots:  ', available_timeslots)
        print('mut_change_exam_prob:  ', mut_change_exam_prob)
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
        print("Algorithm start")
        count_error_child1 = 0
        count_error_child2 = 0
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
                    print('mutant:  ', mutant)
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
        print("Algorithm end")

        # Printing result
        def print_individual(ind):
            print("Printing individual")
            print("Raw:", ind)
            print("Fitness:", ind.fitness.values)

            print(toolbox.evaluate(ind, inverse=False))
            print('meals:  ', meals)
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
                print('Món ăn:  {}  {}'.format(type_food, meals[index].name))
            # for i in range(5):
            #     print('Ngày:  ', i+ 1)
            #
            #     print('Món ăn: Sáng, Xế  ', meals[ind[0 + i]], meals[ind[5+ i]])
            #     print('Món ăn: Sáng 2, Xế 2  ', meals[ind[1+ i]], meals[ ind[6+ i]])
            #     print('Món ăn: canh, xào: ', meals[ind[2+ i]], meals[ ind[7+ i]])
            #     print('Món ăn: mặn: ', meals[ind[3+ i]], meals[ ind[8+ i]])
            #     print('Món ăn: tráng miệng: ', meals[ind[4+ i]], meals[ ind[9+ i]])
            #
            # for index, exam in enumerate(exams):
            #     timeslot = ind[index]
            #     day = timeslot_to_day(timeslot)
            #     slot = timeslot_to_dayslot(timeslot)
            #     print("Exam {} is on day {} - timeslot {}".format(exam, day, slot))

        if print_best:
            print_individual(best_ever)
        return best_ever.fitness.values[0]