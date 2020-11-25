from __future__ import print_function
import random

from deap import base
from deap import creator
from deap import tools


def ga(pop_count, generations_number,
       cx_prob, mut_prob, mut_change_exam_prob,
       evaluate_func, available_timeslots, exams,
       timeslot_to_day, timeslot_to_dayslot,
       print_best, select_method=None):

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    # base.Fitness is a type of deap.
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("random_timeslot", random.randint, 0, available_timeslots - 1)
    # truyền biến vào hàm random_timeslot trong random_timeslot gọi hàm random.randint(), 2 biến 0 và (available_timeslots-1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_timeslot, n=len(exams))
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
    # tập hợp mẫu tạo ra để chọn các cá thể
    best_ever = pop[0]

    # Calculate fitness for first generation
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)
        if ind.fitness.values > best_ever.fitness.values:
            best_ever = toolbox.clone(ind)

    print("Algorithm start")
    for gen in range(generations_number):
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            a = random.random()
            if a < cx_prob:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        # Apply mutation on the offspring
        for mutant in offspring:
            if random.random() < mut_prob:
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

        for index, exam in enumerate(exams):
            timeslot = ind[index]
            day = timeslot_to_day(timeslot)
            slot = timeslot_to_dayslot(timeslot)
            print("Exam {} is on day {} - timeslot {}".format(exam, day, slot))

    if print_best:
        print_individual(best_ever)

    return best_ever.fitness.values[0]
