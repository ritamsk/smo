import numpy
import scipy.stats
import random
import Q_system
import matplotlib.pyplot as plt
import math


n=7
states = n+1
lambd = 0.33
mu = 0.25

TIME = 11
num_of_iters = 10000*10

result = numpy.zeros((TIME, states))
num_of_clients = 0
clients, t_l, t_mu = Q_system.get_clients(TIME, num_of_iters, lambd, mu) #генерация заявок
clients = numpy.array(clients)
for i in range(0, num_of_iters):
    if (i%1000==0):
        print('i', i)

    clients_coming = numpy.array([c['coming_time'] for c in clients[i]])

    channels = numpy.zeros(n)
    result[0, 0] += 1  # начальное состояние системы
    for t in range(1, TIME):

        now = numpy.where(clients_coming == t) #пришедшие сейчас заявки
        num_of_clients += len(now[0])
        working = numpy.array([w['working_time'] for w in clients[i][now]]) #время их обработки

        #print('working', working)
        if len(working) > 0:

            all = len(working)-1
            come = 0
            for ch in range(0, n):
                if channels[ch] == 0:
                    if come <= all:
                        channels[ch] = working[come] #свободный канал берет на обработку пришедшую новую заявку
                        come += 1
                else:
                    channels[ch] -= 1
        else:
            channels[numpy.where(channels > 0)] -= 1

        #print('channels', channels)
        current_state = len(numpy.where(channels > 0)[0])
        #print('current_state', current_state)
        result[t, current_state] += 1 #запоминаем состояние системы

y = numpy.transpose(result/num_of_iters) #считаем частоту

#параметры смо, эксперимент
print('параметры смо, эксперимент')

p_notwork = y[0][TIME-1] # вероятность простоя системы
p_otk = numpy.sum(y[states-1])/TIME #вероятность отказа системы

t_l = t_l #среднее время между заявками
t_mu = t_mu #среднее время обслуживания заявки каналом

q = 1 - p_otk  #относительная пропускная способность системы
A =  (1/t_l)*q #абсолютная пропускная способность системы
k = A/(1/t_mu) #среднее число занятых каналов

t_sys = t_l*k #среднее время нахождения заявки в системе



print('вероятность простоя системы', p_notwork)
print('вероятность отказа системы', p_otk)
print('относительная пропускная способность системы', q)
print('абсолютная пропускная способность системы', A)
print('среднее число занятых каналов', k)
print('среднее время между заявками', t_l)
print('среднее время обслуживания заявки каналом', t_mu)
print('среднее время нахождения заявки в системе', t_sys)

#параметры смо, формулы
print('\nпараметры смо, формулы')
p_tmp = [math.pow((lambd/mu), i) for i in range(0, states)]
p_tmp_1 = [p_tmp[i]/math.factorial(i) for i in range(0, states)]
p_notwork = 1/(numpy.sum(p_tmp_1)) #вероятность простоя системы
p_otk =  (((lambd/mu)**n)/math.factorial(n))*p_notwork #вероятность отказа системы

q = 1 - p_otk #относительная пропускная способность системы
A = lambd*q #абсолютная пропускная способность системы
k = A/mu #среднее число занятых каналов

t_l = 1/lambd #среднее время между заявками
t_mu = 1/mu #среднее время обслуживания заявки каналом
t_sys = t_l*k #среднее время нахождения заявки в системе
t_allwork = 1/(mu*n) #среднее время полной загрузки системы

print('вероятность простоя системы', p_notwork)
print('вероятность отказа системы', p_otk)
print('относительная пропускная способность системы', q)
print('абсолютная пропускная способность системы', A)
print('среднее число занятых каналов', k)
print('среднее время между заявками', t_l)
print('среднее время обслуживания заявки каналом', t_mu)
print('среднее время нахождения заявки в системе', t_sys)



#график

fig, ax = plt.subplots()

x = range(0, TIME)

for i in range(0 , len(y)):
    line = ax.plot(x, y[i], label='state {0}'.format(i))
    ax.legend()

ax.grid(True)
ax.set_xlabel('time')
ax.set_ylabel('frequency')
plt.show()

