"""Exact arithmetic checks for the documentation, not a complete FFT test."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json


def roundshift(x, shift):
    assert shift > 0
    return (-1 if x < 0 else 1) * ((abs(x) + (1 << (shift-1))) >> shift)


def saturate(x):
    return min(max(x, -32768), 32767)


def butterfly(a, b, w):
    product = (b[0]*w[0]-b[1]*w[1], b[0]*w[1]+b[1]*w[0])
    t = tuple(roundshift(v, 16) for v in product)
    us = tuple(roundshift(a[k]+t[k], 1) for k in range(2))
    vs = tuple(roundshift(a[k]-t[k], 1) for k in range(2))
    clips = sum(v < -32768 or v > 32767 for v in us+vs)
    return tuple(map(saturate,us)),tuple(map(saturate,vs)),dict(product_f31=product,rotation_f15=t,u_before_saturation=us,v_before_saturation=vs,clipped_components=clips)


def main():
    checks=[]
    u,v,t=butterfly((16384,8192),(8192,-4096),(0,-65536))
    assert u==(6144,0) and v==(10240,8192) and t['clipped_components']==0
    # Independent rational calculation for W=-j, with no quantization.
    a=(Fraction(1,2),Fraction(1,4));b=(Fraction(1,4),Fraction(-1,8));rot=(b[1],-b[0])
    assert tuple(Fraction(x,32768) for x in u)==tuple((a[k]+rot[k])/2 for k in range(2))
    assert tuple(Fraction(x,32768) for x in v)==tuple((a[k]-rot[k])/2 for k in range(2))
    checks.append('integer butterfly versus independent rational arithmetic')
    assert [roundshift(x,1) for x in [-3,-1,0,1,3]]==[-2,-1,0,1,2]
    assert roundshift(32768,16)==1 and roundshift(-32768,16)==-1
    checks.append('positive and negative half-LSB ties')
    assert saturate(40000)==32767 and saturate(-40000)==-32768
    assert (40000+32768)%65536-32768==-25536
    checks.append('saturation versus wrap example')
    assert Fraction(32767,32768)<1 and Fraction(-32768,32768)==-1
    assert -131072<=-65536<=65536<=131071
    checks.append('Q1.15 limits and representable unit twiddles')
    perm=[int(f'{i:03b}'[::-1],2) for i in range(8)]
    assert perm==[0,4,2,6,1,5,3,7]
    checks.append('N8 bit-reversal permutation')
    assert 9*(512//2)==2304 and 7*(128//2)==448
    assert Fraction(1,2)**9==Fraction(1,512)
    checks.append('stage counts and accumulated normalization')
    _,_,stress=butterfly((32767,0),(32767,32767),(46341,-46341))
    assert stress['clipped_components']>0
    checks.append('full-scale complex counterexample despite per-stage divide by two')
    root=Path(__file__).resolve().parents[2]
    result=dict(evidence='THEORETICAL documentation checks; no MATLAB execution or complete FFT validation',
        checks_passed=checks,u_codes=u,v_codes=v,trace=t,stress=stress,
        matlab_example_sha256=hashlib.sha256((root/'simulation/matlab/demo_fixed_butterfly.m').read_bytes()).hexdigest())
    print(json.dumps(result,indent=2))
    (Path(__file__).parent/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
