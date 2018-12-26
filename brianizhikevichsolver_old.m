% Created by Pranav Malhotra, 07/06/2017
% Before calling script, initialise variables f, t, n, N, horizon, sparsity, diffusion_type, r, m
% f: name of file with fired nodes
% t: name of file with the corresponding firing times
% n: name of file with the network
% N: number of nodes
% horizon: horizon after firings to consider spread
% sparsity: sparsity of the network
% diffusion_type: Either 'exp', 'rayleigh', 'pl'
% r: name of file to store results in
% m: name of file to store inferred matrix

seed=1;
num_nodes=10;
sparsity=0.1;
simulation_duration=4000;
networkFileName='r/for_histogram/network_sim_time_1000/network_seed_1.csv';
f='w/firing.csv';
t='w/indice.csv';
r='r/for_histogram/network_sim_time_4000/results.txt';
n='r/for_histogram/network_sim_time_4000/network_seed_1.csv'; 
fileToTrackProgress='r/for_histogram/network_sim_time_4000/progress_tracker_seed_1.txt';
m = 'r/for_histogram/network_sim_time_4000/matlab_inferred_matrix_seed_1.csv';
diffusion_type='rayleigh';
horizon=100;
num_processors=3;
N = num_nodes;

%  read all the files obtained in python
firings_indices=csvread(f);
firing_times=csvread(t);
network=csvread(n);

% obtain adjacency matrix
S=zeros(int32(N),int32(N));
for i=1:size(network,1)
    S(network(i,1)+1,network(i,2)+1)=network(i,3);
end

% initiliase vector to hold cascades
cascades=[];

% extract cascades for each node in the network
% assuming that all nodes are stimulated
for n=1:N
    % cycle through all firings
    for i=1:size(firings_indices,2)-1
        
        % skip if node is not the stimulated node
        if(firings_indices(n,i)~=n-1 || firing_times(n,i)==0)
            continue
        end
        
        % define the window of observation
        start=firing_times(n,i);
        end_of_period=start+horizon;

        % find the location of all the nodes that fired in the window
        index=find(firing_times(n,:)>start & firing_times(n,:)<end_of_period);
        % collate the fired nodes
        firings_in_window=firings_indices(n,index);
        firings_in_window(2,:)=firing_times(n,index)-start;
        firings_in_window=firings_in_window';
        % initialise a cascade, non-fired with -1; assume all non-fired
        current_cascade=ones(1,N)*-1;
        % stimulated nodde starts the cascade
        current_cascade(firings_indices(n,i)+1)=0;
        % update cascade based on the rest of the firings
        for k=1:length(firings_in_window(:,1))
            % if 1 node fires twice in an observation winddow,
            % only the first one is considered
            if(current_cascade(firings_in_window(k,1)+1)==-1)
                current_cascade(firings_in_window(k,1)+1)=firings_in_window(k,2);
            end
        end
        % all to cascades
        cascades=[cascades;current_cascade];
    end
end

% file handle for writing results
progressTrackerHandle=fopen(fileToTrackProgress,'a');

% estimate the network
S_hat = estimate_network_old(S, cascades, N, horizon, diffusion_type, progressTrackerHandle);
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