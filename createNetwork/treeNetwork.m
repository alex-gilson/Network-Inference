%Author: Roxana Irina Alexandru (ria12)
%Email: rialexandru01@gmail.com
%University: Imperial College London
%Description: Function which creates a tree network 
%Inputs:
%1. Number of children of each node: C
%2. Depth of tree: D
%Outputs: Adjancency matrix adjMatrix
function [N, adjMatrix ] = treeNetwork( D, C )

N=1;
X=1;
%Number of nodes
for i=1:(D-1)
    X=X*C;
    N=N+X;
end

M=zeros(N,N);

%Select the index of the source node
src=1;

%Connect the source node 1
for c=2:(C+1)
    M(1,c)=1;
    M(c,1)=1;
end

for k=2:(D-1)
    lower=((C^(k-1)-1)/(C-1))+1;
    upper=(C^(k)-1)/(C-1);
    const=C^(k-1);
    for i=lower:upper
        for j=1:C
        e=lower+const+(i-lower)*C+j-1;
        M(i,e)=1;
        M(e,i)=1;
        end
    end
end


adjMatrix=M;
end

