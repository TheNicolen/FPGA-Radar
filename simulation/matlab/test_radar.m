function results = test_radar()
% Eight assertion groups. Run in MATLAB; no toolboxes required.
p=radar_config(); q=fmcw_parameters(p); rng(p.seed,'twister');
a=antenna_link(p,[1000 2000]);
assert(abs(a.rx_gain_dbi-18.82)<0.1);
assert(abs(diff(a.received_dbm)+40*log10(2))<1e-9);
p2=p;p2.fc_hz=5.8e9;p2.max_speed_mps=20;
b=antenna_link(p2,1000);
assert(abs(a.received_dbm(1)-b.received_dbm)<1e-9); % fixed TX gain/aperture RX
results.link_scaling=true;
assert(q.max_beat_hz<p.sample_rate_hz/2 && q.unambiguous_speed_mps>40);
bad=p;bad.sample_start_s=0; caught=false;
try, fmcw_parameters(bad); catch, caught=true; end
assert(caught); results.parameter_guards=true;
for velocity=[0,10*q.speed_bin_mps,-10*q.speed_bin_mps]
    x=synth_iq(p,[600 velocity 0.5],0);
    [P,ax]=range_doppler(p,x); [~,idx]=max(P(:)); [ir,id]=ind2sub(size(P),idx);
    corrected=p.c*(ax.beat_hz(ir)-ax.doppler_hz(id))/(2*q.slope_hz_s);
    assert(abs(corrected-600)<=q.observed_range_resolution_m);
    assert(abs(ax.velocity_mps(id)-velocity)<q.speed_bin_mps/2);
end
results.static_and_signed_doppler=true;
x=synth_iq(p,[300 0 0.5;700 0 0.4],0);[P,ax]=range_doppler(p,x);
for R=[300 700]
    mask=abs(ax.range_apparent_m-R)<2*q.observed_range_resolution_m;
    rows=find(mask);[~,j]=max(P(mask,p.chirps/2+1));
    assert(abs(ax.range_apparent_m(rows(j))-R)<=q.observed_range_resolution_m);
end
results.two_separated_targets=true;
[z,clips]=quantize_iq([0.123+0.32j,2-2j],12);
assert(abs(z(1)-(0.123+0.32j))<=sqrt(2)/2^12 && clips==2);
results.quantizer=true;
x=synth_iq(p,[600 0 0.5],0);[xq,clips]=quantize_iq(x,16);
assert(clips==0);[A,~]=range_doppler(p,x);[B,~]=range_doppler(p,xq);
[~,ia]=max(A(:));[~,ib]=max(B(:));assert(ia==ib);
results.quantized_input_peak=true;
[d,t]=ca_cfar_1d([ones(20,1);100;ones(20,1)],8,2,1e-3);
assert(d(21) && ~any(d(1:10)) && isnan(t(1)));
results.cfar_geometry=true;
% Independent groups avoid treating correlated sliding decisions as IID.
trials=50000; n=16; pfa=0.01;
noise=-log(max(rand(trials,n+1),realmin)); alpha=n*(pfa^(-1/n)-1);
observed=mean(noise(:,1)>alpha*mean(noise(:,2:end),2));
assert(abs(observed-pfa)<5*sqrt(pfa*(1-pfa)/trials));
results.cfar_iid_pfa=observed;
results.assertion_groups=8;disp(results);
end
