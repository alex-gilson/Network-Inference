#!/usr/local/bin/bash

seed="$1"
num_nodes="$2"
sparsity="$3"
simulation_duration="$4"
networkFileName="$5"
firingsFileName="$6"
indicesFileName="$7"
resultsFileName="$8"
matlabNetworkFileName="$9"
pythonNetworkFileName="${10}"
fileToTrackProgress="${11}"

echo "Seed:$seed,num_nodes:$num_nodes,sparsity:$sparsity,n=$networkFileName,f:$firingsFileName,i:$indicesFileName" >> $resultsFileName

./izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName

echo "Done with simulation, Starting Matlab"

./utility.py $networkFileName &

time matlab -nodesktop -nosplash -nojvm -r "f='$firingsFileName';t='$indicesFileName';n='$networkFileName';N=$num_nodes;horizon=20;sparsity=$sparsity;diffusion_type='exp';r='$resultsFileName';m='$matlabNetworkFileName';fileToTrackProgress='$fileToTrackProgress';brianIzhikevichSolver;exit" 1> /dev/null

echo "Done with Matlab, Printing Graph"

echo >> $resultsFileName

sed -i '' '1d' $matlabNetworkFileName

./compare_networks.py $networkFileName $matlabNetworkFileName 0 $num_nodes &

./arrange_data_for_python.sh

time ./cvxpy_netrate_parallel.py $num_nodes $pythonNetworkFileName

./compare_networks.py $networkFileName $pythonNetworkFileName 1 $num_nodes &

