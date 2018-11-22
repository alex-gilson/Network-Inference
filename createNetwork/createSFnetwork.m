ccc;

%Number of nodes
N = 200;

%Size of seed network
mo = 20;

%Average degree of seed network
d = 4;

%Adjacency Matrix
% M = BAgraph_dir(N,mo,d);
%M = SFgraph( d, mo, N);
 M = SFBarabasiModel(N);

figure
G = graph(M);
h = plot(G, 'Layout', 'force');


% Find all shortest paths between any two nodes
D = zeros(N,N);
parfor i = 1:N
    for j = 1:N
        D(i,j) = dijkstra(M,i,j);
    end
end
