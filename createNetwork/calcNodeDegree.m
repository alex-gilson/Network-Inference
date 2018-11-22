function [ degree ] = calcNodeDegree(N, M, i )
degree = 0;
for j = 1:N
    if M(i,j) == 1
        degree = degree+1;
    end
end
end

