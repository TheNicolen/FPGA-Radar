function [detected,threshold] = ca_cfar_1d(power,training_each,guard_each,pfa)
% CA-CFAR reference on LINEAR power; no edge wrap/padding.
assert(isvector(power) && all(power(:)>=0));
assert(training_each>=1 && training_each==fix(training_each));
assert(guard_each>=0 && guard_each==fix(guard_each));
assert(pfa>0 && pfa<1);
power=power(:); n=2*training_each; alpha=n*(pfa^(-1/n)-1);
threshold=nan(size(power)); detected=false(size(power));
h=training_each+guard_each;
for k=h+1:numel(power)-h
    indices=[k-h:k-guard_each-1,k+guard_each+1:k+h];
    threshold(k)=alpha*mean(power(indices));
    detected(k)=power(k)>threshold(k);
end
% Nominal Pfa assumes IID exponential training and CUT. Windowed maps differ.
end
