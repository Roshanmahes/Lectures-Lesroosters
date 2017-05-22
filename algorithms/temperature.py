import math

END_TEMP = 0.00001
MAX_BRIDGE = 1
SIG_CONST = 20
ITER_THRESHOLD = 100000
REHEATS = 5

def linear(temperature, total_iters, i, start_temp):
    return temperature - (start_temp - END_TEMP) / total_iters

def exponential(temperature, total_iters, i, start_temp):
    return temperature * (END_TEMP / start_temp) ** (1 / total_iters)

def sigmoidal(temperature, total_iters, i, start_temp):
    return (start_temp - END_TEMP)/(1 + math.exp(SIG_CONST*i/total_iters - SIG_CONST/2)) + END_TEMP

def geman(temperature, total_iters, i, start_temp):
    return MAX_BRIDGE/(math.log(i+1) + 1)

def lin_sig(temperature, total_iters, i, start_temp):
    if i < total_iters/2:
        return linear(temperature, total_iters, i, start_temp)
    return sigmoidal(temperature, total_iters, i, start_temp)

def exp_sig_full(temperature, total_iters, i, start_temp):
    if i < ITER_THRESHOLD:
        return exponential(temperature, total_iters, i, start_temp)
    return sigmoidal(temperature, total_iters - ITER_THRESHOLD, i - ITER_THRESHOLD, start_temp)

def exp_sig_part(temperature, total_iters, i, start_temp):
    if i < ITER_THRESHOLD:
        return exponential(temperature, total_iters, i, start_temp)
    return sigmoidal(temperature, total_iters, i, start_temp)

def exp_reheat(temperature, total_iters, i, start_temp):
    for j in range(REHEATS-1,-1,-1):
        if i == int(total_iters * j/REHEATS):
            return start_temp * (1 - j/REHEATS)
        elif i > int(total_iters * j/REHEATS):
            return exponential(temperature, total_iters * (1 - j/REHEATS), \
                    i - total_iters * (j/REHEATS), start_temp * (1 - j/REHEATS))
