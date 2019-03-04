% 
% 
% function generate_cascades_real(f, t, n, N, horizon, sparsity, diffusion_type, r, m, fileToTrackProgress)
% 
% end
% Load the data
data = load('CRCNS/data/DataSet4.mat');
data = data.data;

% Count the number of spikes in the whole dataset
number_spikes = 0;

for n=1:size(data.spikes,1)
    number_spikes = number_spikes + size(data.spikes{n},2);
end
disp(number_spikes);

