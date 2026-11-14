function summary = run_study(outdir)
% Reproducible first study. Outputs are synthetic/theoretical, never measured.
if nargin<1, outdir=fullfile(fileparts(mfilename('fullpath')),'..','results','matlab'); end
if ~exist(outdir,'dir'),mkdir(outdir);end
p=radar_config();rng(p.seed,'twister');q=fmcw_parameters(p);
summary.config=p;summary.derived=q;summary.matlab_version=version;
summary.tests=test_radar();summary.link_1km=antenna_link(p,1000);
summary.evidence='TEORICO and SIMULADO; no physical measurements';
% Sensitivity: frequency, aperture efficiency, RCS. Separate fixed TX gain.
rows=[];
for f=[2.4e9 2.45e9 5.8e9]
 for eta=[0.35 0.55 0.70]
  for rcs=[1 10 100]
   pp=p;pp.fc_hz=f;pp.aperture_efficiency=eta;pp.rcs_m2=rcs;
   if f>3e9,pp.max_speed_mps=20;end
   a=antenna_link(pp,1000);
   rows(end+1,:)=[f eta rcs a.rx_gain_dbi a.received_dbm a.snr_ideal_bin_db a.threshold_range_m]; %#ok<AGROW>
  end
 end
end
writetable(array2table(rows,'VariableNames',{'frequency_hz','efficiency','rcs_m2', ...
 'rx_gain_dbi','received_dbm_1km','ideal_bin_snr_db_1km','threshold_range_m'}),fullfile(outdir,'sensitivity.csv'));
f=figure('Visible','off');R=linspace(50,2500,300);
for rcs=[1 10 100]
 pp=p;pp.rcs_m2=rcs;a=antenna_link(pp,R);plot(R,a.snr_ideal_bin_db,'LineWidth',1.5);hold on;
end
yline(p.threshold_snr_db,'--');grid on;xlabel('Range (m)');ylabel('Ideal coherent-bin SNR (dB)');
title('THEORETICAL: ideal coherence, no clutter');legend('RCS 1 m2','RCS 10 m2','RCS 100 m2','Illustrative threshold');
exportgraphics(f,fullfile(outdir,'theoretical_range.png'));close(f);
% Deliberately high normalized SNR for algorithm verification, NOT link proof.
rng(p.seed,'twister');x=synth_iq(p,[600 20 0.5],1e-3);[P,ax]=range_doppler(p,x);
[~,idx]=max(P(:));[ir,id]=ind2sub(size(P),idx);
summary.synthetic_peak.range_corrected_m=p.c*(ax.beat_hz(ir)-ax.doppler_hz(id))/(2*q.slope_hz_s);
summary.synthetic_peak.velocity_mps=ax.velocity_mps(id);
[xq,clips]=quantize_iq(x,16);summary.quantization_clipped_components=clips;
f=figure('Visible','off');imagesc(ax.velocity_mps,ax.range_apparent_m,10*log10(P+realmin));axis xy;
ylim([0 1100]);xlabel('Velocity (m/s)');ylabel('Apparent range (m)');colorbar;
title('SIMULATED: normalized target 600 m, +20 m/s');
exportgraphics(f,fullfile(outdir,'synthetic_range_doppler.png'));close(f);
% Small deterministic first-chirp vector; entire input cube stays out of Git.
writematrix([real(xq(:,1)),imag(xq(:,1))],fullfile(outdir,'iq_first_chirp_q15.csv'));
save(fullfile(outdir,'study.mat'),'p','q','summary','xq','P','ax');
fid=fopen(fullfile(outdir,'summary.json'),'w','n','UTF-8');assert(fid>=0);
c=onCleanup(@() fclose(fid));fprintf(fid,'%s\n',jsonencode(summary,'PrettyPrint',true));
disp(summary.derived);disp(summary.link_1km);
end
