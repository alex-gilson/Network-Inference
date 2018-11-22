function [ M ] = SFgraph( d, mo, N)
%The average degree of the initial network is d
%Create initial graph of m0 nodes
M = zeros(N,N);
for i = 1:mo
    neighbours = randi(d);
    for n = 1:neighbours
        j = randi(i);
        if j~=i
            M(j,i) = 1;
            M(i,j) = 1;
        else
            M(j,i) = 0;
            M(i,j) = 0;
        end
    end
end

for i = mo+1:N
    degsum = 0;
    deg = zeros(1,i-1);
    p = zeros(1,i-1);
    %Look at all pre-existing nodes
    for j = 1: i-1
        %Calculate degree of node j
        deg(j) = calcNodeDegree(N, M,j);
        degsum = degsum + deg(j);
    end
    
    for j = 1: i-1
        %Calculate probability of connection to each node j
        p(j) = deg(j)/degsum;
        %Generate a connection with probability p(j) between node j and
        %node i

        %Probability of connection
        prob2 = p(j);
        
        %Probability of not being infected by rumor
        prob1 = 1-p(j);

        %Probability vector
        prob=[prob1, prob2];

        %Vector with N random values between 0 and 1
        r=rand(1,1);
        C = cumsum([0, prob]);
        s = sum( r>=cumsum([0,prob]) );
        randVector=sum( r>=cumsum([0,prob]) )-1;
        M(i,j) = randVector;
        M(j,i) = randVector;

    end
    
end


end

