
function [a_hat, obj] = solve_using_cvx(i, type_diffusion, num_nodes, num_cascades, A_potential, A_bad, C)
    cvx_begin quiet
    cvx_expert true
    
        % optimisation variables, objects, not yet numbers
        % after the problem is solved, these will become numbers
        % a_hat(num_nodes) is a vector
        variable a_hat(num_nodes);
        % defining a vector that is as long as the number of cascades a
        % particular node i was infected in. Again we are not counting the
        % node if it was randomly picked to be the root node
        variable t_hat(num_cascades(i));
        
        % defining the object function, which is the maximum likelihood of
        % a cascade happening
        obj = 0;
    
        % == is the relational operator that imposes constraints
        % = would give an error; would interpret it as an assignment
        % this constraint is saying that if within any cascades, a node j
        % never occured before a node i (in this scenario, A_ji == 0) then 
        % in the approximation of A, there should not be any edge from node
        % j to node i
        % In the paper, this is talked about as the Unfeasible Rate
        a_hat(A_potential(:,i)==0) == 0;
                
        for j=1:num_nodes
            if (A_potential(j,i) > 0)
                % traverse the A_potential and A_bad matrix down 1
                % particular column, and sum up the log survival functions
                obj = -a_hat(j)*(A_potential(j,i) + A_bad(j,i)) + obj;
            end
        end
        
        % this is simply a counting variable
        % the next for loop is iterating over all of the cascades, however
        % a particular node i does not appear in all of the casdes. We have
        % instantiated a variable t_hat(num_cascades(i)), which is the
        % length of the number of cascades that a variable appears in. To
        % add stuff to this vector, we need to keep a count variable.
        c_act = 1;
        
        
        % size(C, 1) will return the number of cascades
        % this is because C is such that number of rows = number of cascades
        % traversing through the number of cascades
        for c=1:size(C, 1)
            % finds nodes in 1 row of C that are not equal to -1
            % idx finds the nodes that were present in that particular cascade
            idx = find(C(c,:)~=-1);
            
            % sorts the cascades so that the nodes are arranged in increasing order
            % of hit times
            [val, ord] = sort(C(c, idx));
    
            % order all the nodes based on the time that they were
            % infected.
            idx_ord = idx(ord);
            
            % find the node that we are currently looking at, i.e., the ith
            % node
            cidx = find(idx_ord==i);
            
            % if:
            % ~isempty(cidx) -> if node i appeared in current cascade
            % cidx > 1 -> if node i was not the randomly chosen root node
            if (~isempty(cidx) && cidx > 1)
                % Here we are looking at the hazard functions and adding
                % them up
                if (strcmp(type_diffusion, 'exp'))
                    % idx_ord(1:cidx-1) will return the nodes that appeared
                    % in the cascade prior to node i 
                    % This line is defining a constraint on the sum of
                    % hazard functions.
                    % This term cannot be 0 because we log it later.
                    % This ensure that for node i to be infected, at least
                    % one of the previously infected nodes have to have a
                    % branch to the node.
                    t_hat(c_act) == sum(a_hat(idx_ord(1:cidx-1)));
                elseif (strcmp(type_diffusion, 'pl'))       
                    tdifs = 1./(val(cidx)-val(1:cidx-1));
                    % in the paper, for the power law, delta was defined to
                    % 1 without loss of generality 
                    indv = find(tdifs<1);
                    tdifs = tdifs(indv);
                    t_hat(c_act) <= (tdifs*a_hat(idx_ord(indv)));
                elseif (strcmp(type_diffusion, 'rayleigh'))
                    tdifs = (val(cidx)-val(1:cidx-1)); 
                    t_hat(c_act) <= (tdifs*a_hat(idx_ord(1:cidx-1)));
                end
                
                % add the hazard functions into the objective function,
                % which is the likelihood of a set of cascades happening
                obj = obj + log(t_hat(c_act));

                c_act = c_act + 1;
            end
        end

        % sets the constraint that each element of a_hat has to be
        % positive. This cis shown in the paper in equation number 9.
        a_hat >= 0;
        
        % maximise the likelihood function
        maximize obj
    cvx_end
end
