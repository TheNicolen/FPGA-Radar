"""Independent stdlib reference; does NOT execute or validate MATLAB syntax."""
import cmath
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import re

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'results' / 'python_reference'

def config():
    text = (HERE / 'radar_config.m').read_text(encoding='utf-8')
    return {key: float(value) for key, value in re.findall(r'p\.(\w+)\s*=\s*([0-9.eE+-]+)\s*;', text)}

def fft(x):
    n = len(x)
    assert n and n & (n-1) == 0
    y = list(x)
    j = 0
    for i in range(1,n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            y[i], y[j] = y[j], y[i]
    size = 2
    while size <= n:
        step = cmath.exp(-2j*math.pi/size)
        for start in range(0,n,size):
            w = 1
            for k in range(start,start+size//2):
                t = w*y[k+size//2]
                y[k+size//2] = y[k]-t
                y[k] += t
                w *= step
        size *= 2
    return y

def parameters(p):
    lam = p['c']/p['fc_hz']
    slope = p['bandwidth_hz']/p['chirp_duration_s']
    n,m = int(p['samples']),int(p['chirps'])
    obs = n/p['sample_rate_hz']
    tau = 2*p['max_range_m']/p['c']
    fb = slope*tau+2*p['max_speed_mps']/lam
    vmax = lam/(4*p['chirp_interval_s'])
    dr = p['c']/(2*slope*obs)
    assert tau <= p['sample_start_s']
    assert p['sample_start_s']+obs <= p['chirp_duration_s']+1e-12
    assert fb < .8*p['sample_rate_hz']/2
    assert p['max_speed_mps'] < vmax
    assert p['max_speed_mps']*m*p['chirp_interval_s'] < .25*dr
    return dict(wavelength_m=lam,slope_hz_s=slope,max_beat_hz=fb,
        nominal_resolution_m=p['c']/(2*p['bandwidth_hz']),observed_resolution_m=dr,
        range_bin_m=p['c']*p['sample_rate_hz']/(2*slope*p['range_fft_size']),
        velocity_bin_mps=lam/(2*m*p['chirp_interval_s']),unambiguous_speed_mps=vmax,
        frame_s=m*p['chirp_interval_s'],raw_frame_bytes=n*m*2*p['adc_bits']/8,
        fft_cube_bytes_32bit_components=p['range_fft_size']*m*8,
        cycles_per_sample=p['fpga_clock_hz']/p['sample_rate_hz'],
        geometric_gate_limit_m=p['c']*p['sample_start_s']/2)

def link(p,R):
    q=parameters(p)
    area=math.pi*p['aperture_width_m']*p['aperture_height_m']/4
    gr=p['aperture_efficiency']*4*math.pi*area/q['wavelength_m']**2
    # Independent linear watts expression rather than the .m dB equation.
    received=(10**((p['tx_power_dbm']-30)/10)*10**(p['tx_gain_dbi']/10)*gr
        *q['wavelength_m']**2*p['rcs_m2']/((4*math.pi)**3*R**4*10**(p['loss_db']/10)))
    noise=1.380649e-23*p['temperature_k']*p['sample_rate_hz']*10**(p['noise_figure_db']/10)
    weights=[[.5-.5*math.cos(2*math.pi*k/int(p[key])) for k in range(int(p[key]))]
        for key in ['samples','chirps']]
    gain=math.prod(sum(w)**2/sum(x*x for x in w) for w in weights)
    snr=10*math.log10(received/noise*gain)
    return dict(rx_gain_dbi=10*math.log10(gr),received_dbm=10*math.log10(received)+30,
        noise_dbm=10*math.log10(noise)+30,coherent_gain_db=10*math.log10(gain),
        ideal_bin_snr_db=snr,energy_threshold_range_m=R*10**((snr-p['threshold_snr_db'])/40))

def quantize(x,bits=16):
    scale=2**(bits-1)
    def matlab_round(v): return math.copysign(math.floor(abs(v)+.5),v)
    z=[matlab_round(v*scale) for v in [x.real,x.imag]]
    clips=sum(v < -scale or v > scale-1 for v in z)
    return complex(*[min(max(v,-scale),scale-1)/scale for v in z]),clips

def simulate(p,targets,quantized=False):
    q=parameters(p);n,m,nf=map(int,[p['samples'],p['chirps'],p['range_fft_size']])
    wr=[.5-.5*math.cos(2*math.pi*k/n) for k in range(n)]
    wd=[.5-.5*math.cos(2*math.pi*k/m) for k in range(m)]
    columns=[]
    for j in range(m):
        col=[]
        for k in range(n):
            t=p['sample_start_s']+k/p['sample_rate_hz']
            z=0j
            for R,v,A in targets:
                tau=2*R/p['c'];fd=2*v/q['wavelength_m']
                phase=(q['slope_hz_s']*tau+fd)*t+fd*j*p['chirp_interval_s']+p['fc_hz']*tau-.5*q['slope_hz_s']*tau*tau
                z+=A*cmath.exp(2j*math.pi*phase)
            if quantized: z=quantize(z)[0]
            col.append(z*wr[k])
        columns.append(fft(col+[0j]*(nf-n)))
    power=[]
    for k in range(nf//2):
        z=fft([columns[j][k]*wd[j] for j in range(m)])
        z=z[m//2:]+z[:m//2]
        power.append([abs(v/(sum(wr)*sum(wd)))**2 for v in z])
    ir,id=max(((i,j) for i in range(nf//2) for j in range(m)),key=lambda ij:power[ij[0]][ij[1]])
    fd=(id-m/2)/(m*p['chirp_interval_s']);fb=ir*p['sample_rate_hz']/nf
    result=dict(range_corrected_m=p['c']*(fb-fd)/(2*q['slope_hz_s']),velocity_mps=fd*q['wavelength_m']/2,range_bin=ir,doppler_bin=id)
    return result,power

def main():
    p=config();q=parameters(p);a=link(p,1000);checks=[]
    # Verify the independent FFT against direct DFT, not another FFT.
    x=[complex(k,-k/3) for k in range(8)]
    direct=[sum(x[j]*cmath.exp(-2j*math.pi*k*j/8) for j in range(8)) for k in range(8)]
    assert max(abs(a-b) for a,b in zip(fft(x),direct))<1e-10
    checks.append('FFT versus direct DFT')
    assert abs(link(p,2000)['received_dbm']-a['received_dbm']+40*math.log10(2))<1e-10
    assert abs(link(dict(p,fc_hz=5.8e9,max_speed_mps=20),1000)['received_dbm']-a['received_dbm'])<1e-10
    checks.append('link R^-4 and fixed-TX/RX-aperture frequency invariance')
    try: parameters(dict(p,sample_start_s=0));raise RuntimeError('Guard did not reject invalid input')
    except AssertionError: pass
    checks.append('timing and alias parameter guards')
    peaks=[]
    for v in [0,10*q['velocity_bin_mps'],-10*q['velocity_bin_mps']]:
        peak,_=simulate(p,[(600,v,.5)])
        assert abs(peak['range_corrected_m']-600)<=q['observed_resolution_m']
        assert abs(peak['velocity_mps']-v)<q['velocity_bin_mps']/2
        peaks.append(peak)
    checks.append('static and signed Doppler recovery')
    _,power=simulate(p,[(300,0,.5),(700,0,.4)])
    for R in [300,700]:
        candidates=[i for i in range(len(power)) if abs(i*q['range_bin_m']-R)<2*q['observed_resolution_m']]
        i=max(candidates,key=lambda i:power[i][int(p['chirps'])//2])
        assert abs(i*q['range_bin_m']-R)<=q['observed_resolution_m']
    checks.append('two separated synthetic targets')
    z,clips=quantize(2-2j,12);assert clips==2 and z.real==1-2**-11 and z.imag==-1
    z,clips=quantize(.123+.32j,12);assert clips==0 and abs(z-(.123+.32j))<=math.sqrt(2)/2**12
    checks.append('quantization and saturation')
    peak,_=simulate(p,[(600,0,.5)],True)
    assert (peak['range_bin'],peak['doppler_bin'])==(peaks[0]['range_bin'],peaks[0]['doppler_bin'])
    checks.append('Q1.15 input peak matches floating reference')
    rng=random.Random(int(p['seed']));trials=50000;n=16;pfa=.01
    alpha=n*(pfa**(-1/n)-1);hits=0
    for _ in range(trials):
        cut=rng.expovariate(1);training=sum(rng.expovariate(1) for _ in range(n))/n
        hits+=cut>alpha*training
    observed=hits/trials
    assert abs(observed-pfa)<5*math.sqrt(pfa*(1-pfa)/trials)
    checks.append('CA-CFAR IID exponential false-alarm probability')
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[]
    for fc in [2.4e9,2.45e9,5.8e9]:
        for eta in [.35,.55,.7]:
            for rcs in [1,10,100]:
                pp=dict(p,fc_hz=fc,aperture_efficiency=eta,rcs_m2=rcs,max_speed_mps=20 if fc>3e9 else 40)
                rows.append(dict(fc_hz=fc,efficiency=eta,rcs_m2=rcs,**link(pp,1000)))
    with (OUT/'sensitivity.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    result=dict(engine='Python stdlib independent reference, NOT MATLAB execution',python=platform.python_version(),
        configuration=p,derived=q,link_1km=a,passed_checks=checks,synthetic_peaks=peaks,
        cfar_iid=dict(trials=trials,pfa_target=pfa,pfa_observed=observed),
        source_sha256={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(HERE.glob('*.m'))},
        limitations='Ideal theory and synthetic data; no physical or FPGA validation. This independent engine does not execute MATLAB source.')
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
