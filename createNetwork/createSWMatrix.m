%Author: Roxana Irina Alexandru (ria12)
%Email: rialexandru01@gmail.com
%University: Imperial College London
%Description:Generation of a Small-world network
%Parameters:
%1.Number of Nodes : N
%2.Average vertex degree (2K) : K
%3.Rewiring probability: beta
%Outputs:
%1. Adjancency matrix M
%2. Matrix of shortest distances D

ccc;
%The number of nodes is N
N = 20;

%Node degree is 2K
K = 2;

%Rewiring probability
beta = 0.2;

%Select the index of the source node
src = 1;

%Create a matrix describing the graph structure

%h=WattsStrogatz(N,K, beta);
M = WattsStrogatz(N,K,beta);

figure
G = graph(M);
h = plot(G, 'Layout', 'force');

D = zeros(N,N);
SM = sparse(M);

%Find all shortest paths between any two nodes
parfor i = 1:N
    for j = 1:N
        D(i,j) = graphshortestpath(SM, i, j);
    end
end
