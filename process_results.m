function process_results(sparsity, r, diffusion_type, resultsFileHandle, num_nodes, m)

S = csvread('w/S_matrix.csv');
cascades = csvread('w/cascades.csv');

% Get the number of nodes from the size of the adjacency matrix S
size_S = size(S);
num_nodes = S(2);
S_hat = zeros(size_S);

% Obtain each of the columns of the estimated adjacency matrix
for n = 1:num_nodes
	S_hat(:,n) = csvread(strcat('temporary/a_hat_',int2str(n), '.csv'));
end
disp(S_hat);
% threshold based on defined level of sparsity
S_hat=pranav_threshold_sparsity(S_hat, sparsity);

% file handle for writing results
resultsFileHandle=fopen(r,'a');

% obtain the metrics
pranav_get_metrics(S,S_hat,diffusion_type,resultsFileHandle, cascades);

% close the File
fclose(resultsFileHandle);

% obtain estimated adjacency matrix
S_hat_adjacency=digraph(S_hat);

% write information to file
writetable(S_hat_adjacency.Edges, m);
