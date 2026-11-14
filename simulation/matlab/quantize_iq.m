function [y, clipped_components] = quantize_iq(x,bits)
% Signed normalized Q1.(bits-1), including sign; round then saturate.
assert(bits>=2 && bits<=24 && bits==fix(bits));
scale=2^(bits-1);
i=round(real(x)*scale); q=round(imag(x)*scale);
clipped_components=nnz(i < -scale | i > scale-1)+nnz(q < -scale | q > scale-1);
y=(min(max(i,-scale),scale-1)+1j*min(max(q,-scale),scale-1))/scale;
% FFT arithmetic remains floating point; this is NOT a fixed-point FFT.
end
