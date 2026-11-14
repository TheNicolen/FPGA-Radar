function q = fmcw_parameters(p)
% TEORICO: feasibility constraints for an ideal dechirped IF input.
assert(p.fc_hz>0 && p.bandwidth_hz>0 && p.sample_rate_hz>0);
assert(p.samples==fix(p.samples) && p.samples>=4);
assert(p.chirps==fix(p.chirps) && p.chirps>=4 && mod(p.chirps,2)==0);
assert(p.range_fft_size>=p.samples && p.range_fft_size==fix(p.range_fft_size));
assert(p.chirp_interval_s>=p.chirp_duration_s);
q.lambda_m = p.c/p.fc_hz;
q.slope_hz_s = p.bandwidth_hz/p.chirp_duration_s;
q.max_delay_s = 2*p.max_range_m/p.c;
assert(p.sample_start_s>=q.max_delay_s,'Sampling starts before the farthest same-chirp echo.');
q.observation_s = p.samples/p.sample_rate_hz;
assert(p.sample_start_s+q.observation_s<=p.chirp_duration_s+1e-12);
q.max_doppler_hz = 2*p.max_speed_mps/q.lambda_m;
q.max_beat_hz = q.slope_hz_s*q.max_delay_s+q.max_doppler_hz;
assert(q.max_beat_hz<0.8*p.sample_rate_hz/2,'Insufficient anti-alias transition margin.');
q.nominal_range_resolution_m = p.c/(2*p.bandwidth_hz);
q.observed_range_resolution_m = p.c/(2*q.slope_hz_s*q.observation_s);
q.range_bin_m = p.c*p.sample_rate_hz/(2*q.slope_hz_s*p.range_fft_size);
q.speed_bin_mps = q.lambda_m/(2*p.chirps*p.chirp_interval_s);
q.unambiguous_speed_mps = q.lambda_m/(4*p.chirp_interval_s);
assert(p.max_speed_mps<q.unambiguous_speed_mps);
q.frame_s = p.chirps*p.chirp_interval_s;
q.max_migration_m = p.max_speed_mps*q.frame_s;
assert(q.max_migration_m<0.25*q.observed_range_resolution_m,'Stop-and-hop approximation too coarse.');
q.raw_frame_bytes = p.samples*p.chirps*2*p.adc_bits/8;
q.fft_cube_bytes_at_32_bits_per_component = p.range_fft_size*p.chirps*2*32/8;
q.peak_iq_bits_s = p.sample_rate_hz*2*p.adc_bits;
q.cycles_per_input_sample = p.fpga_clock_hz/p.sample_rate_hz;
q.frame_cycles = p.fpga_clock_hz*q.frame_s;
q.radix2_butterflies_per_frame = p.chirps*p.range_fft_size/2*log2(p.range_fft_size) ...
    + p.range_fft_size*p.chirps/2*log2(p.chirps);
% No estimate here covers memory stalls, twiddle latency, CFAR or routing.
end
