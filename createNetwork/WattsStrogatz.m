%Author: Roxana Irina Alexandru (ria12)
%Email: rialexandru01@gmail.com
%University: Imperial College London
%Description:
% H = WattsStrogatz(N,K,beta) returns a Watts-Strogatz model graph with N
% nodes, N*K edges, mean node degree 2*K, and rewiring probability beta.
% beta = 0 means a ring lattice, and beta = 1 means a random graph.
function [ M ] = WattsStrogatz( N,K,beta )


%Adjacency Matrix
M=zeros(N,N);

% Connect each node to its K next and previous neighbors. This constructs
% indices for a ring lattice.
%Create matrix of K repeated rows
%On each row
s = repelem((1:N)',1,K);
t = s + repmat(1:K,N,1);
t = mod(t-1,N)+1;

% Rewire the target node of each edge with probability beta
%The source is the current node we are looking at
for source=1:N    
    switchEdge = rand(K, 1) < beta;
    
    newTargets = rand(N, 1);
    %Avoid self-loops
    newTargets(source) = 0;
    %Look at the previous K neighbors of source and set the connection to 0
    %i.e. get the indices for which t=source
    newTargets(s(t==source)) = 0;
    %Find the connections to the next K neighbors and set some of them to
    %0, according to probability Beta
    newTargets(t(source, ~switchEdge)) = 0;
    %The last 2K nodes in the ind vector are the next and previous neighbors
    %Which do not need to be re-wired
    [~, ind] = sort(newTargets, 'descend');
    %nnz returns the number of non-zero matrix elements
    %For those neighbors for which switchEdge=1, i.e. which need to be
    %rewired, create a new edge to other 2 random nodes
    t(source, switchEdge) = ind(1:nnz(switchEdge));
end

for i = 1:N
    for k = 1:K
    j=t(i,k);
    M(i,j)=1;
    M(j,i)=1;
    end
end

end