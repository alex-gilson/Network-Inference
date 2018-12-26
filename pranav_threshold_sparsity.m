function S_hat=pranav_threshold_sparsity(S, sparsity_level)
    
    % initialize sparse matrix
    S_hat=full(S);
   
    % get number of neurons in network
    N=size(S_hat,1);
      
    % remove terms that are nan
    S_hat(isnan(S_hat))=0;
    
    % sort values 
    [sortedValues,~]=sort(vec(S_hat),'descend');
    
    % compute the threshold beyond which all terms are set to 0
    %cutOff=sortedValues(floor(sparsity_level*N*N));
    cutOff=sortedValues(floor(sparsity_level*N*N));
    
    % threshold
    S_hat(S_hat<cutOff)=0;
    
end
