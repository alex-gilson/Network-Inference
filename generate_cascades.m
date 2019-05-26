% Created by Pranav Malhotra, 07/06/2017, edited by Alejandro Gilson 21/12/2018
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
% Setup the cvx package so that it can be used
%run('/home/alex/Downloads/cvx/cvx_setup.m');

function generate_cascades(f, t, n, N, horizon, sparsity, diffusion_type, r, m, fileToTrackProgress)


% seed=1;
% num_nodes=10;
% sparsity=0.1;
% simulation_duration=4000;
% networkFileName='r/for_histogram/network_sim_time_1000/network_seed_1.csv';
% f='w/firing.csv';
% t='w/indice.csv';
% r='r/for_histogram/network_sim_time_4000/results.txt';
% n='r/for_histogram/network_sim_time_4000/network_seed_1.csv'; 
% fileToTrackProgress='r/for_histogram/network_sim_time_4000/progress_tracker_seed_1.txt';
% diffusion_type='rayleigh';
% horizon=100;
% num_processors=3;
%
%  read all the files obtained in python
firings_indices=csvread(f);
firing_times=csvread(t);
network=csvread(n);

% obtain adjacency matrix
S=zeros(int32(N),int32(N));
for i=1:size(network,1)
    S(network(i,1)+1,network(i,2)+1)=network(i,3);
end

num_nodes = N;
% initialize a vector to hold the cascades
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

        % stimulated node starts the cascade
        current_cascade(firings_indices(n,i)+1)=0;

        % update cascade based on the rest of the firings
        for k=1:length(firings_in_window(:,1))
            % if 1 node fires twice in an observation window,
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

num_cascades = zeros(1,num_nodes);
A_potential = zeros(size(S));
A_bad = zeros(size(S));
A_hat = zeros(size(S));
total_obj = 0;

tic
for c=1:size(cascades, 1)
    % Obtain the timing of the nodes that have fired
    idx = find(cascades(c,:)~=-1); % used nodes
    
    % Sort each cascade by earliest firing and keep the index order (ord)
    [val, ord] = sort(cascades(c, idx));
    
    % For all used nodes
    % Don't take the first value (it's value is 0, it belongs to the
    % stimulated node)
    
    for i=2:length(val)
		
        % num_cascades stores the amount of times each node has fired
        num_cascades(idx(ord(i))) = num_cascades(idx(ord(i))) + 1;
        for j=1:i-1
            if (strcmp(diffusion_type, 'exp'))
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+val(i)-val(j);
            elseif (strcmp(diffusion_type, 'pl') && (val(i)-val(j)) > 1)
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+log(val(i)-val(j));
            elseif (strcmp(diffusion_type, 'rayleigh'))
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+0.5*(val(i)-val(j))^2;
            end
        end
    end
    
    for j=1:num_nodes
        if isempty(find(idx==j))
            for i=1:length(val)
                if (strcmp(diffusion_type, 'exp'))
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + (horizon-val(i));
                elseif (strcmp(diffusion_type, 'pl') && (horizon-val(i)) > 1)
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + log(horizon-val(i));
                elseif (strcmp(diffusion_type, 'rayleigh'))
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + 0.5*(horizon-val(i))^2;
                end
            end
        end
    end
end
stop=toc;

csvwrite('w/a_potential.csv',full(A_potential))
csvwrite('w/a_bad.csv',full(A_bad))
csvwrite('w/cascades.csv',full(cascades))
csvwrite('w/num_cascades.csv',full(num_cascades))
csvwrite('w/S_matrix.csv',full(S))

fprintf(progressTrackerHandle,'Done Arranging Data, Took %.3f seconds\n\n', stop);

