function a = antenna_link(p,range_m)
% TEORICO: equivalent monostatic free-space radar, fixed TX gain.
assert(all(range_m(:)>0) && p.rcs_m2>0);
assert(p.aperture_efficiency>0 && p.aperture_efficiency<=1);
q=fmcw_parameters(p);
a.projected_area_m2=pi*p.aperture_width_m*p.aperture_height_m/4;
a.rx_gain_linear=p.aperture_efficiency*4*pi*a.projected_area_m2/q.lambda_m^2;
a.rx_gain_dbi=10*log10(a.rx_gain_linear);
a.received_dbm=p.tx_power_dbm+p.tx_gain_dbi+a.rx_gain_dbi ...
    +20*log10(q.lambda_m)+10*log10(p.rcs_m2)-30*log10(4*pi) ...
    -40*log10(range_m)-p.loss_db;
% Ideal complex white noise with integrated equivalent bandwidth Fs.
a.noise_dbm=10*log10(1.380649e-23*p.temperature_k*p.sample_rate_hz)+30+p.noise_figure_db;
wr=0.5-0.5*cos(2*pi*(0:p.samples-1)'/p.samples);
wd=0.5-0.5*cos(2*pi*(0:p.chirps-1)/p.chirps);
a.coherent_gain_linear=sum(wr)^2/sum(wr.^2)*sum(wd)^2/sum(wd.^2);
a.coherent_gain_db=10*log10(a.coherent_gain_linear);
a.snr_input_db=a.received_dbm-a.noise_dbm;
a.snr_ideal_bin_db=a.snr_input_db+a.coherent_gain_db;
a.threshold_range_m=range_m.*10.^((a.snr_ideal_bin_db-p.threshold_snr_db)/40);
% Ideal on-bin coherent target only: no phase noise, clutter or scalloping.
end
