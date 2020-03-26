import matplotlib.pyplot as plt
from math import *
from cmath import exp, pi
import random

W, N, HARM, AMPL, SHIFT = 2000, 256, 8, random.uniform(0, 1), random.uniform(0, 1)


def get_signal_point(t, w, ampl, sh):
    return sin(w * t + sh) * ampl


def get_dft(n):
    res = list()
    for i in range(len(n)):
        s = 0
        for j in range(len(n)):
            s += n[j] * complex(cos(-2 * pi * j * i / len(n)), sin(-2 * pi * j * i / len(n)))
        res.append(s)
    return res


def get_fft(n):
    l = len(n)
    if l <= 1: return n
    even = get_fft(n[0::2])
    odd = get_fft(n[1::2])
    t = [exp(-2j * pi * i / l) * odd[i] for i in range(l // 2)]
    return [even[i] + t[i] for i in range(l // 2)] + [even[i] - t[i] for i in range(l // 2)]


def get_real(arr):
    return [i.real for i in arr]


def get_imag(arr):
    return [i.imag for i in arr]


if __name__ == "__main__":
    signal = list()

    for i in range(N):
        s = 0
        for j in range(HARM):
            s += get_signal_point(i, W * j / HARM, AMPL, SHIFT)
        signal.append(s)

    new_signal = list()

    for i in range(int(pow(2, 12))):
        s = 0
        for j in range(HARM):
            s += get_signal_point(i, W * j / HARM, AMPL, SHIFT)
        new_signal.append(s)

    time_np_st = time()
    f.fft(new_signal)
    time_np_f = time()
    time_np = time_np_f - time_np_st

    time_my_st = time()
    get_fft(new_signal)
    time_my_f = time()
    time_my = time_my_f - time_my_st

    print(time_np)
    print(time_my)
    print(f"{'Custom FFT' if time_my < time_np else 'Numpy FFT'} is faster")
    plt.subplot(221)
    plt.ylabel('DFT')
    plt.plot(get_real(get_dft(signal)))
    plt.subplot(222)
    plt.plot(get_imag(get_dft(signal)))
    plt.subplot(223)
    plt.ylabel('FFT')
    plt.plot(get_real(get_fft(signal)), "red")
    plt.subplot(224)
    plt.plot(get_imag(get_fft(signal)), "red")

    plt.savefig("plot.png")
