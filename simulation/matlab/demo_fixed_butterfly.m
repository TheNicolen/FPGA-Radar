function result = demo_fixed_butterfly()
% TEORICO: one integer radix-2 butterfly, not a full FFT or RTL model.
% Data signed W16 F15; twiddles signed W18 F16; scale /2.
% Explicit round-to-nearest, ties away from zero; saturate final registers.
a = int64([16384, 8192]);
b = int64([8192, -4096]);
w = int64([0, -65536]);
[u,v,trace] = butterfly(a,b,w);
assert(isequal(u,int64([6144,0])));
assert(isequal(v,int64([10240,8192])));
assert(trace.clipped_components==0);
assert(isequal(roundshift(int64([-3,-1,0,1,3]),1),int64([-2,-1,0,1,2])));
% Counterexample: /2 does not ensure no overflow for every full-scale I/Q.
[~,~,stress] = butterfly(int64([32767,0]),int64([32767,32767]),int64([46341,-46341]));
assert(stress.clipped_components>0);
result.input_a_codes=a; result.input_b_codes=b; result.twiddle_codes=w;
result.output_u_codes=u; result.output_v_codes=v;
result.output_u_value=double(u)/2^15; result.output_v_value=double(v)/2^15;
result.trace=trace; result.stress_clipped_components=stress.clipped_components;
result.evidence='THEORETICAL worked example, not measured radar data';
disp(result);
end

function [u,v,trace] = butterfly(a,b,w)
% int64 is only a safe host container; the intended widths are documented.
assert(all(a>=-32768 & a<=32767) && all(b>=-32768 & b<=32767));
assert(all(w>=-131072 & w<=131071));
product=[b(1)*w(1)-b(2)*w(2), b(1)*w(2)+b(2)*w(1)]; % F31
rotation=roundshift(product,16); % F15, retain widened result
us=roundshift(a+rotation,1); vs=roundshift(a-rotation,1);
trace.product_f31=product; trace.rotation_f15=rotation;
trace.u_before_saturation=us; trace.v_before_saturation=vs;
trace.clipped_components=nnz(us < -32768 | us > 32767)+nnz(vs < -32768 | vs > 32767);
u=min(max(us,int64(-32768)),int64(32767));
v=min(max(vs,int64(-32768)),int64(32767));
end

function q = roundshift(x,s)
% Bounds above keep abs(x) and half-LSB addition well inside int64.
assert(s>=1 && s<=31 && s==fix(s));
q=idivide(abs(x)+bitshift(int64(1),s-1),bitshift(int64(1),s),'floor');
q(x<0)=-q(x<0);
end
