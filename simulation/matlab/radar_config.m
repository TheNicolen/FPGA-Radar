function p = radar_config()
% HIPOTESIS: parameters for study, not approved hardware settings.
p.c = 299792458;
p.fc_hz = 2.45e9;
p.aperture_width_m = 0.46;
p.aperture_height_m = 0.46;
p.aperture_efficiency = 0.55; % Unknown; sensitivity sweep required.
p.tx_gain_dbi = 15; % Separate TX antenna assumed, NOT a second owned dish.
p.tx_power_dbm = 0;
p.rcs_m2 = 10;
p.loss_db = 6;
p.noise_figure_db = 6;
p.temperature_k = 290;
p.threshold_snr_db = 10; % Illustrative threshold, not a Pd/Pfa requirement.
p.bandwidth_hz = 20e6;
p.chirp_duration_s = 256e-6;
p.chirp_interval_s = 300e-6;
p.sample_rate_hz = 2e6; % Complex IF AFTER dechirp and anti-alias filtering.
p.sample_start_s = 8e-6;
p.samples = 480;
p.chirps = 128;
p.range_fft_size = 512;
p.max_range_m = 1000;
p.max_speed_mps = 40;
p.fpga_clock_hz = 100e6; % Design target, not measured Fmax.
p.adc_bits = 16;
p.seed = 20261114;
end
