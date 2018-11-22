function [S_bin, S_hat_bin, mae,recall,precision,accuracy]=pranav_get_metrics(S, S_hat, type_diffusion, resultsFileHandle, cascades)
    
    % initialise binary matrix for S
    S_bin=S;
  
    % make values binary
    S_bin(S_bin>0)=1;
    
    % initalise binary matrix for S_hat
    S_hat_bin=S_hat;
    
    % make values binary
    S_hat_bin(S_hat_bin>0)=1; S_hat_bin(S_hat_bin<=0)=0;
    
    % Compute the difference between the two matrices
    num=S_bin-S_hat_bin;
    
    % set all minus ones to ones 
    num(num==-1)=1;
    
    % remove oddities due to non-convergence of algorithm
    num(isnan(num))=0;
        
    % calulate the MAE
    mae = mean(abs(S_hat(S~=0)-S(S~=0))./S(S~=0));
    
    % calculate the recall
    recall = sum(sum(S_hat_bin & S_bin))/sum(sum(S_hat_bin));
    
    % calculate the precision
    precision = sum(sum(S_hat_bin & S_bin))/sum(sum(S_bin));
    
    % calculate the accuracy
    accuracy=1-sum(sum(num))/(sum(sum(S_bin))+sum(sum(S_hat_bin)));
    
    fprintf(resultsFileHandle,'Method:%s,Accuracy:%.3f,MAE:%.3f,Precision:%.3f,Recall:%.3f,Number of Cascades:%d\n', type_diffusion, accuracy,mae,precision,recall, size(cascades,1));
    
end