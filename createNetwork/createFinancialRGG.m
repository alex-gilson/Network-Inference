ccc;

%Number of companies
N = 200;

%Average degree
d = 10;

U = rand(N,N);
t = d./(N-1);
M = double(U<t).*(ones(N,N)-eye(N));
M = M';


D = zeros(N,N);
%Find all shortest paths between any two nodes
parfor i = 1:N
    for j = 1:N
        D(i,j) = dijkstra(M,i,j);
    end
end
