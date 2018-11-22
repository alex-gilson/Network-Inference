ccc

%The number of nodes is N
N = 200;

%Create a matrix describing the graph structure
[M, Locations, Dist_XY] = rggNetwork(N);

figure
G = graph(M);
h = plot(G, 'Layout', 'force');


% %Create matrix of distances
% % D=shortestPaths(M);
parfor i = 1:N
    for j = 1:N
        D(i,j) = dijkstra(M,i,j);
    end
end 