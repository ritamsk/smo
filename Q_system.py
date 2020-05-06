import random
import math
import scipy.stats
import tmp
import sklearn.preprocessing
import numpy
import random


lambd = 0.33
mu = 0.25

time = 10


def sorting(x):
    return x['coming_time']


def get_clients(time, iters, lambd, mu):
    time = time*2
    all_clients = []
    t_l = 0
    t_mu = 0
    clients_coming = scipy.stats.expon.rvs(size=time*iters, scale=1/lambd)
    random.shuffle(clients_coming)
    #print(clients_coming)
    working_times = scipy.stats.expon.rvs(size=time*iters, scale=1/mu)
    clients_coming = clients_coming.reshape(iters, time)
    working_times = working_times.reshape(iters, time)
    #print(clients_coming.shape)
    for i in range(0, iters):
        clients = []
        t_MU = 0
        t_L = 0

        clients.append({'coming_time': int(round(clients_coming[i][0])), 'working_time':  int(round(working_times[i][0]))})
        t_L += math.ceil(clients_coming[i][0])
        t_MU += math.ceil(working_times[i][0])
        for t in range(1, time):
            client_coming = int(round(clients_coming[i][t]))
            t_L += client_coming
            working_time = int(round(working_times[i][t]))
            t_MU += working_time
            #working_time = math.ceil(working_times[i-1])

            client = {'coming_time': clients[t-1]['coming_time'] + client_coming, 'working_time': working_time}
           # print(i,t, client)
            #print(clients)
           #client = {'coming_time': client_coming, 'working_time': working_time}
            clients.append(client)

        all_clients.append(clients)

        t_l += (t_L/time)
        t_mu += (t_MU/time)
        #clients.sort(key=sorting)
        #clients_coming.sort()
        #print(clients)

    return all_clients, (t_l/iters), (t_mu/iters)


#print(get_clients(time, 50000, lambd, mu))