import random

import numpy as np


def calc_hx711(n_measurement):
    n_mean = n_measurement.mean()
    n_var = n_measurement.var()
    n_std = n_measurement.std()
    print(f'{n_mean=}, {n_var}, {n_std=}')

def calc(x, y):
    try:
        result = x / y
        return result

    except RuntimeError as e:
        print('idiot')
    except ZeroDivisionError:
        print('again')



def main():
    #rand = np.random.sample(0)
    #print(rand)
    #calc_hx711(rand)

    print(calc(10, 0))

if __name__ == '__main__':
    main()