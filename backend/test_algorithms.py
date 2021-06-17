# ЗАДАЧА:
# participants_count - число участников, записавшихся на мероприятие
# teams_count - число команд, установленных организатором
# max_team_size - макс человек в команде
# min_team_size - мин человек в команде
# max_teams - максимальное число команд
# min_teams - минимальное число команд
# value(Ni) - ценность участника, вычисляемая на основе опроса, который проходит участник при записи на мероприятие
# Необходимо распределить N участников на M команд; учитывая ценность каждого участника сформировать оптимальные команды
# с примерно одинаковой конкурентоспособностью
# То есть сумма ценностей участников каждой команды должна быть примерно одинаковой.
# values(1, 2, 3 ,4 ,5 ,6) team_size = 2
# sum1(value1, value2) ~~ sum2(value1, value2) ~~ sum3... ~~ sum4... ...
# команд может от 2 до 10(к примеру)
# 1 команда - уже не командное мероприятие
# PARTITION TO K SUBSETS OF FIXED SIZE WITH MINIMAL SUM DIFFERENCE
import sys
import math
import random


class Participant:
    def __init__(self, data, score):
        self.data = data
        self.score = score


class Team:
    def __init__(self):
        self.name = ''
        self.members = []


# функция распределяет участников по командам
def build_teams():
    scores.sort(reverse=True)
    # закомментированный код позволяет убрать худших участников для равного разделения на команды
    # trash = []
    # while len(scores) / team_size != len(scores) // team_size:
    #     trash.append(scores[-1])
    #     scores.remove(scores[-1])
    # print('Participants_count = ', len(scores))
    partitions = math.ceil(len(scores) / team_size)
    boundary = int(sum(scores) / partitions)
    boundary_offset = 0
    teams = [[] for partition in range(partitions)]
    for i in range(partitions):
        teams[i].insert(i, scores[0])
        scores.remove(scores[0])
    for score in scores:
        assigned = False
        team_index = 0
        while not assigned:
            if (sum(teams[team_index]) + score) <= (boundary + boundary_offset):
                teams[team_index].insert(0, score)
                assigned = True
            else:
                if team_index == (len(teams) - 1):
                    team_index = 0
                    boundary_offset += 1
                else:
                    team_index += 1
    return teams


# функция определяет факт существования команд, превышающих фиксированный размер
def bigger_teams_exist(teams, oversize):
    for team in teams:
        if len(team) > team_size + oversize:
            return True
    return False


# функция возвращает оценку худшего участника среди команд, превышающих фиксированный размер команды
def get_worst_member_score(teams, oversize):
    worst_member_score = max(scores)
    team_index = 0
    for i, team in enumerate(teams):
        if len(team) > team_size + oversize:
            curr_worst_member_score = min(team)
            if curr_worst_member_score < worst_member_score:
                worst_member_score = curr_worst_member_score
                team_index = i
    teams[team_index].remove(worst_member_score)
    return worst_member_score


# функция возвращает худшую команду по сумме оценок участников
# среди команд, число участников в которых меньше фиксированного
def get_worst_of_smaller_teams(teams, oversize):
    worst_team = teams[0]
    for i, team in enumerate(teams):
        if len(team) < team_size + oversize:
            curr_worst_team_score = sum(team)
            if curr_worst_team_score < sum(worst_team):
                worst_team = team
    return worst_team


# функция возвращает худшую команду по суммарному баллу
def get_worst_team(teams):
    worst_team = teams[0]
    for team in teams:
        team_score = sum(team)
        if team_score < sum(worst_team):
            worst_team = team
    return worst_team


# функция возвращает лучшую команду по суммарному баллу
def get_best_team(teams):
    best_team = []
    for team in teams:
        team_score = sum(team)
        if team_score > sum(best_team):
            best_team = team
    return best_team


# фукнция определяет, нужно ли обменивать худшего участника худшей команды и лучшего участника лучшей команды
# для минимизации разницы суммарных оценок лучшей и худшей команд
def t_need_exchange(teams):
    best_team = get_best_team(teams)
    worst_team = get_worst_team(teams)
    score_diff = sum(best_team) - sum(worst_team)
    print('best_member = ', max(best_team), 'score_diff = ', score_diff)
    return max(best_team) < score_diff


def need_exchange(teams):
    best_team = get_best_team(teams)
    worst_team = get_worst_team(teams)
    score_diff = sum(best_team) - sum(worst_team)
    print('best_member = ', max(best_team), 'score_diff = ', score_diff)
    return score_diff > 0


# функция обменивает двух участников в командах
def exchange(teamA, teamB, scoreA, scoreB):
    teamA.remove(scoreA)
    teamA.append(scoreB)
    teamB.remove(scoreB)
    teamB.append(scoreA)


# функция сначала разбивает участников на команды с помощью исходного алгоритма,
# затем оптимизирует число участников в команде, учитывая максимально возможную
# разницу между числом участников в командах(oversize)
def build_fixed_teams(oversize=0):
    teams = build_teams()
    while bigger_teams_exist(teams, oversize):
        worst_score = get_worst_member_score(teams, oversize)
        worst_team = get_worst_of_smaller_teams(teams, oversize)
        worst_team.append(worst_score)

    # пока в лучшей команде оценка лучшего участника меньше чем разница суммарных оценок лучшей и худшей команды
    # нужно обменивать лучшего участника лучшей команды с худшим участником худшей команды
    # если вдруг разница оценок новых лучшей и худшей команд будет больше препдыдущей -
    # то происходит откат(обмен) к предыдущему составу команд,затем выход из цикла
    while need_exchange(teams):
        best_team = get_best_team(teams)
        worst_team = get_worst_team(teams)
        prev_difference = abs(sum(best_team) - sum(worst_team))
        best_score = max(best_team)
        worst_score = min(worst_team)
        exchange(best_team, worst_team, best_score, worst_score)
        curr_best_team = get_best_team(teams)
        curr_worst_team = get_worst_team(teams)
        curr_difference = abs(sum(curr_best_team) - sum(curr_worst_team))
        if curr_difference > prev_difference:
            exchange(best_team, worst_team, worst_score, best_score)
            break
    return teams


def build_fixed_teams2(oversize=0):
    teams = build_teams()
    while bigger_teams_exist(teams, oversize):
        worst_score = get_worst_member_score(teams, oversize)
        worst_team = get_worst_of_smaller_teams(teams, oversize)
        worst_team.append(worst_score)

    # пока в лучшей команде оценка лучшего участника меньше чем разница суммарных оценок лучшей и худшей команды
    # нужно обменивать лучшего участника лучшей команды с худшим участником худшей команды
    # если вдруг разница оценок новых лучшей и худшей команд будет больше препдыдущей -
    # то происходит откат(обмен) к предыдущему составу команд,затем выход из цикла
    score_index = 0
    while need_exchange(teams):
        best_team = get_best_team(teams)
        worst_team = get_worst_team(teams)
        prev_difference = abs(sum(best_team) - sum(worst_team))
        best_team.sort(reverse=True)
        best_score = best_team[score_index]
        worst_team.sort(reverse=True)
        worst_score = worst_team[team_size - 1 - score_index]
        exchange(best_team, worst_team, best_score, worst_score)
        curr_best_team = get_best_team(teams)
        curr_worst_team = get_worst_team(teams)
        curr_difference = abs(sum(curr_best_team) - sum(curr_worst_team))
        if curr_difference >= prev_difference:
            exchange(best_team, worst_team, worst_score, best_score)
            if score_index + 1 < team_size:
                score_index += 1
            else:
                break
    return teams


def build_fixed_teams3(oversize=0):
    teams = build_teams()
    while bigger_teams_exist(teams, oversize):
        worst_score = get_worst_member_score(teams, oversize)
        worst_team = get_worst_of_smaller_teams(teams, oversize)
        worst_team.append(worst_score)

    # пока в лучшей команде оценка лучшего участника меньше чем разница суммарных оценок лучшей и худшей команды
    # нужно обменивать лучшего участника лучшей команды с худшим участником худшей команды
    # если вдруг разница оценок новых лучшей и худшей команд будет больше препдыдущей -
    # то происходит откат(обмен) к предыдущему составу команд,затем выход из цикла
    team_index = 0
    while need_exchange(teams):
        teams = sorted(teams, key=sum, reverse=True)
        best_team = teams[team_index]
        worst_team = teams[-1]
        sum_difference = abs(sum(best_team) - sum(worst_team))
        exchanged = False
        for j, member1 in enumerate(best_team):
            for k, member2 in enumerate(worst_team):
                if 0 < member1 - member2 < sum_difference:
                    exchange(best_team, worst_team, member1, member2)
                    exchanged = True
                    break
            if exchanged:
                break
        if not exchanged:
            if team_index + 2 < team_size:
                team_index += 1
            else:
                break
        # Берём лучшую и худшую команду, если текущий элемент лучшей команды превышает элемент худшей команды на
        # число, меньшее разницы сумм команд (121 - 110 = 11 если элемент лучшей команды <= 11 / 2 )
    return teams


# сравнение элеметов лучшей команды со всеми элементами остальных команд,
def build_fixed_teams4(oversize=0):
    teams = build_teams()
    while bigger_teams_exist(teams, oversize):
        worst_score = get_worst_member_score(teams, oversize)
        worst_team = get_worst_of_smaller_teams(teams, oversize)
        worst_team.append(worst_score)

    # пока в лучшей команде оценка лучшего участника меньше чем разница суммарных оценок лучшей и худшей команды
    # нужно обменивать лучшего участника лучшей команды с худшим участником худшей команды
    # если вдруг разница оценок новых лучшей и худшей команд будет больше препдыдущей -
    # то происходит откат(обмен) к предыдущему составу команд,затем выход из цикла
    team_index = 0
    teams_count = len(teams)
    print('Число команд: ', teams_count)
    while need_exchange(teams):
        teams = sorted(teams, key=sum, reverse=True)
        best_team = teams[team_index]
        exchanged = False
        for i, team in enumerate(teams):
            if i > team_index:
                sum_difference = abs(sum(best_team) - sum(team))
                if sum_difference > 0:
                    for member1 in best_team:
                        for member2 in team:
                            if 0 < member1 - member2 < sum_difference:
                                exchange(best_team, team, member1, member2)
                                exchanged = True
                                break
                        if exchanged:
                            break
        if not exchanged:
            if team_index + 1 < teams_count - 1:
                team_index += 1
            else:
                break
        # Берём лучшую и другую команды => если текущий элемент лучшей команды превышает элемент другой команды на
        # число, меньшее разницы сумм команд (a_score - b_score <= |121 - 110| = 11 )
    return teams


# random.seed(18)
scores = []
for i in range(1, 101):
    scores.append(random.randint(1, 50))
# scores = list(range(1000))
# scores = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print(scores)
team_size = 4


def print_results():
    # teams = build_teams()
    teams = build_fixed_teams4()
    # teams = sorted(teams, key=len, reverse=True)
    print('-' * 70)
    for team in teams:
        team.sort()
    max_team_sum_diff = 0  # разность суммарных оценок лучшей и худшей команд
    max_team_score = sum(teams[0])  # оценка лучшего участника команды
    min_team_score = sum(teams[0])  # оценка худшего участника команды
    for team in teams:
        team_score = sum(team)
        if team_score > max_team_score:
            max_team_score = team_score
        elif team_score < min_team_score:
            min_team_score = team_score
        print('{} {} {} {} {}'.format(team, ' sum = ', team_score, " size = ", len(team)))
    max_team_sum_diff = max_team_score - min_team_score  # это надо минимизировать
    print("max teams sum difference: ", max_team_sum_diff)


print_results()

# print(timeit.timeit(build_fixed_teams2, number=1))


# может получиться так, что среди всех участников будет только один сильный участник, например [1, 1, 1, 1, 1, 1, 1, 9]
# в таком случае не существует справедливого распределения на команды
# Поэтому если стоит галочка -  фиксированное число участников в каждой команде -
# после работы основного алгоритма среди участников команд, по размеру превышающих фиксированное число участников,
# нужно найти наименее ценных участников и переместить их в команды с недостающим числом участников
