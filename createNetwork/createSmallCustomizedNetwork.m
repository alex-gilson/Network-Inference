ccc;
M = [0 1 1 1; 1 0 1 0; 1 1 0 1; 1 0 1 0];
N = 4;

M = [0 1 0; 1 0 1; 0 1 0];
N = 3;

M = [0 1 0 1; 1 0 1 1; 0 1 0 0; 1 1 0 0];
N = 4;

D = zeros(N,N);
SM = sparse(M);

%Find all shortest paths between any two nodes
parfor i = 1:N
    for j = 1:N
        D(i,j) = graphshortestpath(SM, i, j);
    end
end