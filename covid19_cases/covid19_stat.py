import sys
import csv
import matplotlib.pyplot as plt


if sys.argv[1:]:
    stat_file = sys.argv[1]
else:
    sys.exit("E: $python covid19_stat.py files/COVID19_UA_statistic_December2020.csv")

stat_lines = []

with open(stat_file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    stat_lines = [cr for cr in csv_reader]

labels = stat_lines[0]
del stat_lines[0]

month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
"Июль", "Август", "Сентябрь","Октябрь", "Ноябрь", "Декабрь"]
current_month = month_names[int(stat_lines[0][0].split('.')[1]) - 1]

days = [sl[0].split('.')[0] for sl in stat_lines]
new_cases = [int(sl[1]) for sl in stat_lines]
recovered =  [int(sl[2]) for sl in stat_lines]
hospitalized = [int(sl[3]) for sl in stat_lines]
deaths = [int(sl[4]) for sl in stat_lines]

plt.plot(days, new_cases, marker='o', color='red')
plt.plot(days, hospitalized, marker='o', color='yellow')
plt.plot(days, recovered, marker='o', color='green')
plt.plot(days, deaths, marker='o', color='grey')

plt.suptitle("COVID19 в Украине\n", fontsize=14, fontweight='bold')
plt.title(
	f"За {current_month} 2020.",
	fontsize=10)
plt.legend(
	[
	    f"Новых случаев ({sum(new_cases)} за мес.)",
	    f"Госпитализировано ({sum(hospitalized)} за мес.)",
	    f"Выздоровели ({sum(recovered)} за мес.)",
	    f"Умерло ({sum(deaths)} за мес.)"
	], loc=0)

plt.show()
