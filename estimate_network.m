function [A_hat, total_obj] = estimate_network(A, cascades, num_nodes, horizon, type_diffusion, progressTrackerHandle)

num_cascades = zeros(1,num_nodes);
A_potential = zeros(size(A));
A_bad = zeros(size(A));
A_hat = zeros(size(A));
total_obj = 0;

tic
for c=1:size(cascades, 1)
    % Obtain the timing of the nodes that have fired
    idx = find(cascades(c,:)~=-1); % used nodes
    
    % Sort each cascade by earliest firing and keep the index order (ord)
    [val, ord] = sort(cascades(c, idx));
    
    % For all used nodes
    % Don't take the first value (it's value is 0, it belongs to the
    % stimulated node)
    
    for i=2:length(val)
		
        % num_cascades stores the amount of times each node has fired
        num_cascades(idx(ord(i))) = num_cascades(idx(ord(i))) + 1;
        for j=1:i-1
            if (strcmp(type_diffusion, 'exp'))
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+val(i)-val(j);
            elseif (strcmp(type_diffusion, 'pl') && (val(i)-val(j)) > 1)
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+log(val(i)-val(j));
            elseif (strcmp(type_diffusion, 'rayleigh'))
                A_potential(idx(ord(j)), idx(ord(i))) = A_potential(idx(ord(j)), idx(ord(i)))+0.5*(val(i)-val(j))^2;
            end
        end
    end
    
    for j=1:num_nodes
        if isempty(find(idx==j))
            for i=1:length(val)
                if (strcmp(type_diffusion, 'exp'))
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + (horizon-val(i));
                elseif (strcmp(type_diffusion, 'pl') && (horizon-val(i)) > 1)
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + log(horizon-val(i));
                elseif (strcmp(type_diffusion, 'rayleigh'))
                    A_bad(idx(ord(i)), j) = A_bad(idx(ord(i)), j) + 0.5*(horizon-val(i))^2;
                end
            end
        end
    end
end
stop=toc;

csvwrite('w/a_potential.csv',full(A_potential))
csvwrite('w/a_bad.csv',full(A_bad))
csvwrite('w/cascades.csv',full(cascades))
csvwrite('w/num_cascades.csv',full(num_cascades))
csvwrite('w/S_matrix.csv',full(A))

fprintf(progressTrackerHandle,'Done Arranging Data, Took %.3f seconds\n\n', stop);


% we will have a convex program per column

for i=1:num_nodes
    
    if (num_cascades(i)==0)
        A_hat(:,i) = 0;
        continue;
    end
    
    tic
    [a_hat, obj] = solve_using_cvx(i, type_diffusion, num_nodes, num_cascades, A_potential, A_bad, cascades);
    %C = cascades;
    
    stop=toc;
    
    fprintf(progressTrackerHandle,'Done with node:%d, Took %.3f seconds\n',i, stop);
    %disp('Done with node:%d, Took %.3f seconds\n',i, stop);
    total_obj = total_obj + obj;
    A_hat(:,i) = a_hat;
end
