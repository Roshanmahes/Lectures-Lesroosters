from math import exp, log

# Temperature functions to be used by simulated_annealing.py

START_TEMP = 1
END_TEMP = 0.00001
SIG_CONST = 20
REHEATS = 4

def linear(temperature, total_iters, i):
    return temperature - (START_TEMP - END_TEMP) / total_iters

def exponential(temperature, total_iters, i, start=START_TEMP):
    return temperature * (END_TEMP / start) ** (1 / total_iters)

def sigmoidal(temperature, total_iters, i):
    return END_TEMP + (START_TEMP - END_TEMP)/(1 + \
            exp(SIG_CONST*i/total_iters - SIG_CONST/2))

def geman(temperature, total_iters, i):
    return START_TEMP/(log(i+1) + 1)

def lin_sig(temperature, total_iters, i):
    if i < total_iters/2:
        return linear(temperature, total_iters, i)
    return sigmoidal(temperature, total_iters, i)

def exp_sig_full(temperature, total_iters, i):
    if i < total_iters/2:
        return exponential(temperature, total_iters, i)
    return sigmoidal(temperature, total_iters - total_iters/2, \
            i - total_iters/2)

def exp_sig_part(temperature, total_iters, i):
    if i < total_iters/2:
        return exponential(temperature, total_iters, i)
    return sigmoidal(temperature, total_iters, i)

def exp_reheat(temperature, total_iters, i):
    for j in range(REHEATS-1,-1,-1):
        if i == int(total_iters * j/REHEATS):
            return START_TEMP * (1 - j/REHEATS)
        elif i > int(total_iters * j/REHEATS):
            return exponential(temperature, total_iters * (1 - j/REHEATS), \
                    i - total_iters * (j/REHEATS), START_TEMP * (1 - j/REHEATS))

def exp_lin(temperature, total_iters, i):
    if i == int(total_iters/2):
        return START_TEMP/2
    elif i < total_iters/2:
        return exponential(temperature, total_iters, i)
    else:
        return linear(temperature, total_iters, i)
