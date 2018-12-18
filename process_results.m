function process_results(sparsity, r, S, diffustion_type, resultsFileHandle, cascades)
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
