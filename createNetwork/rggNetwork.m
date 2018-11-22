function [ AdjMatrix, Locations,Dist_XY ] = rggNetwork( N )
% Generate a simple random geome tric graph (network)
%Choose Radius=Dimension to have fully connected graph
Radius = 0.15;

Dimension = 1;

Locations = Dimension*rand(N,2); % Generate 2D locations

% Compute adjacency matrix

Locations_X = Locations(:,1)*ones(1,N);

Locations_Y = Locations(:,2)*ones(1,N);

Dist_XY = ((Locations_X-Locations_X.').^2 + ...
(Locations_Y-Locations_Y.').^2);

AdjMatrix = (Dist_XY <= (Dimension*Radius)^2);

AdjMatrix = AdjMatrix - diag(diag(AdjMatrix));

end

