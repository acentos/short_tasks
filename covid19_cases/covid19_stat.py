import os
import csv
import matplotlib.pyplot as plt


stat_file = 'COVID19_UA_statistic_November2020.csv'
stat_file_path = os.path.join('files', stat_file)

stat_lines = []

with open(stat_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    stat_lines = [cr for cr in csv_reader]

labels = stat_lines[0]
del stat_lines[0]

month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
"Июль", "Август", "Сентябрь","Октябрь", "Ноябрь", "Декабрь"]
current_month = month_names[int(stat_lines[0][0].split('.')[1]) - 1]

days = [sl[0].split('.')[0] for sl in stat_lines][1:]
new_cases = [int(sl[1]) for sl in stat_lines][1:]
recovered =  [int(sl[2]) for sl in stat_lines][1:]
hospitalized = [int(sl[3]) for sl in stat_lines][1:]
deaths = [int(sl[4]) for sl in stat_lines][1:]

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
