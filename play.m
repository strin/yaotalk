fid = fopen('buffer.raw');
x = fread(fid, inf, 'short');
sound(x/max(abs(x)),32000)