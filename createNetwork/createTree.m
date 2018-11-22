ccc;

%The depth of the tree
D = 5;

%The number of children of each node
C = 3;

%Create a matrix describing the graph structure
[N,M] = treeNetwork(D,C);


%Create matrix of distances
D = zeros(N,N);
for i = 1:N
    for j = 1:N
        D(i,j) = dijkstra(M,i,j);
    end
end