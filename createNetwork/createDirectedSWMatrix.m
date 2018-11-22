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

%ccc;
%The number of nodes is N
N = 10;

%Node degree is 2K
degree = 2;

%Rewiring probability
beta = 0.2;

%Select the index of the source node
src = 1;

%Create a matrix describing the graph structure

%h=WattsStrogatz(N,K, beta);
A = WattsStrogatz(N,degree,beta);
for n = 1:N
    for m = 1:N
        if A(m,n) == 1
            A(n,m) = 0;
        end
    end
end


noEdge = 1; 
list = [];
for n = 1:N
    for m = 1:N
        if A(n,m) == 1
            list(noEdge,1) = n-1;
            list(noEdge,2) = m-1;
            noEdge = noEdge+1;
        end
    end
end
csvwrite('network.csv',list);


figure
G = digraph(A);
h = plot(G, 'Layout', 'force');
