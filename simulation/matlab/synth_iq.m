function x = synth_iq(p, targets, noise_power)
% SIMULATION MODEL: dechirped stop-and-hop complex IF, not sampled RF.
% targets rows: [range_m, radial_velocity_mps, complex_amplitude].
% Positive velocity = positive Doppler (approaching under this convention).
q=fmcw_parameters(p);
assert(noise_power>=0);
t=p.sample_start_s+(0:p.samples-1)'/p.sample_rate_hz;
slow=(0:p.chirps-1)*p.chirp_interval_s;
x=complex(zeros(p.samples,p.chirps));
for k=1:size(targets,1)
    R=targets(k,1); v=targets(k,2); A=targets(k,3);
    assert(isreal(R) && isreal(v) && R>0 && R<=p.max_range_m);
    assert(abs(v)<=p.max_speed_mps);
    tau=2*R/p.c; fd=2*v/q.lambda_m;
    assert(tau<=p.sample_start_s);
    % Constant delay over CPI; valid only under the migration check above.
    phase=(q.slope_hz_s*tau+fd)*t+fd*slow+p.fc_hz*tau-0.5*q.slope_hz_s*tau^2;
    x=x+A*exp(1j*2*pi*phase);
end
x=x+sqrt(noise_power/2)*(randn(size(x))+1j*randn(size(x)));
end
