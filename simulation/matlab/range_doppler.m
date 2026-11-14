function [power_map, axes_out] = range_doppler(p,x)
% Floating reference: periodic Hann -> range FFT -> Doppler FFT -> power.
q=fmcw_parameters(p);
assert(isequal(size(x),[p.samples,p.chirps]));
wr=0.5-0.5*cos(2*pi*(0:p.samples-1)'/p.samples);
wd=0.5-0.5*cos(2*pi*(0:p.chirps-1)/p.chirps);
y=fft(x.*wr,p.range_fft_size,1);
y=fftshift(fft(y.*wd,p.chirps,2),2)/(sum(wr)*sum(wd));
y=y(1:floor(p.range_fft_size/2),:);
power_map=abs(y).^2;
axes_out.beat_hz=(0:size(y,1)-1)'*p.sample_rate_hz/p.range_fft_size;
axes_out.doppler_hz=(-p.chirps/2:p.chirps/2-1)/(p.chirps*p.chirp_interval_s);
axes_out.range_apparent_m=axes_out.beat_hz*p.c/(2*q.slope_hz_s);
axes_out.velocity_mps=axes_out.doppler_hz*q.lambda_m/2;
% Correct range for each selected detection: c*(fb-fd)/(2*S).
end
