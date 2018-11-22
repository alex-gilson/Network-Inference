%Author: Roxana Irina Alexandru (ria12)
%Email: rialexandru01@gmail.com
%University: Imperial College London
%Description: Function which generates a scale-free network using the
%Barabasi algorithm, with fixed degree distribution
%Inputs: Number of nodes (must be a power of 3)
%Outputs: Adjancency network M
function [ M ] = SFBarabasiModel( N )
M = zeros(N,N);

%Pick a random initial node, the root of the graph
root = 1;

%Number of iterations
L = (log(N)/log(3)) ;

%Initial unit has no connections and a single node
A = zeros(1,1);

for l = 1:L
    P = A;
    sprev = 3^(l-1)+1;
    snew = 3^l;
 
    %Update the unit
    A = zeros(snew,snew);
    for i = 1:sprev-1
        for j = 1:i;
            A(i,j) = P(i,j);
            %ensure symmetric
            A(j,i) = A(i,j);
        end
    end
    
    for i = sprev : 2*3^(l-1)
        for j = sprev:i
            A(i,j) = P(i-sprev+1,j-sprev+1);
            A(j,i) = A(i,j);
        end
        %Last 2^(k-1) new nodes should be connected to the root
        if i>= (2*3^(l-1)-2^(l-1)) && i<=(2*3^(l-1))
        A(i,root) = 1;
        A(root,i) = 1;
        end
    end
    
    for i = 2*3^(l-1)+1:snew
        for j = 2*3^(l-1)+1:i
            A(i,j) = P(i-2*3^(l-1),j-2*3^(l-1));
            A(j,i) = A(i,j);
        end
        if i>= (snew-2^(l-1)) && i<=snew
        A(i,root) = 1;
        A(root,i) = 1;
        end
    end
end

M = A;

end

