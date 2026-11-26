"""Decode and analyse one fixed-size complex sample block."""
import cmath
import math
import struct

IQ_HEADER = struct.Struct('!4sIII')
IQ_DATA = struct.Struct('!128h')


def decode_iq(data):
    if len(data) < IQ_HEADER.size:
        raise ValueError('Cabecera I/Q corta')
    magic, seq, ticks, fs = IQ_HEADER.unpack_from(data)
    count = {b'RADQ': 64, b'RSC1': 128}.get(magic)
    if count is None or not fs or len(data) != IQ_HEADER.size + 4*count:
        raise ValueError('Cabecera o tamaño I/Q incorrecto')
    values = struct.unpack_from('!{}h'.format(2*count),data,IQ_HEADER.size)
    iq = tuple(complex(i, q)/32768 for i, q in zip(values[::2], values[1::2]))
    return {'seq': seq, 'ticks': ticks, 'fs': fs, 'iq': iq}


def spectrum(block):
    """Two-sided complex DFT, coherent normalization for a bin-centred tone."""
    iq = block['iq']
    n = len(iq)
    freqs, levels = [], []
    for k in range(-n//2, n//2):
        amplitude = abs(sum(x*cmath.exp(-2j*math.pi*k*i/n)
                            for i,x in enumerate(iq))/n)
        freqs.append(k*block['fs']/n)
        levels.append(max(-100, 20*math.log10(max(amplitude, 1e-10))))
    return freqs, levels
