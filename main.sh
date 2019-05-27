# !/usr/local/bin/bash

seed="$1"
num_nodes="$2"
sparsity="$3"
simulation_duration="$4"
networkFileName="$5"
firingsFileName="$6"
indicesFileName="$7"
resultsFileName="$8"
matlabNetworkFileName="$9"
fileToTrackProgress="${10}"
diffusion_type="${11}"
horizon="${12}"
num_processors="${13}"
stimulation_type="${14}"

mkdir temporary
# Activate virtual environment
. py27env/bin/activate

if [ ! -f $networkFileName ] || [ ! -f $firingsFileName ] || [ ! -f $indicesFileName ]
then
	python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName

else
	echo -e "Found Brian Simulator files"
fi

echo -e "\tGenerating cascades..."

python generate_cascades.py $num_nodes $indicesFileName $firingsFileName $diffusion_type $horizon $simulation_duration

# Get current time and store it into a pickle file
python initial_time.py

echo -e "\tComputing Netrate..." 

python parallelize_cvx.py $num_processors $num_nodes $horizon $diffusion_type $fileToTrackProgress

echo -e "Processing results..."

python compare_networks.py $num_nodes $networkFileName 1

echo -e "Calculating elapsed time..."

python final_time.py $resultsFileName $seed $num_nodes $sparsity $networkFileName $firingsFileName $indicesFileName $matlabNetworkFileName $fileToTrackProgress $horizon $num_processors $diffusion_type $stimulation_type 

rm initial_time.pickle
# rm temporary/*

echo "Results are available at '$resultsFileName'"
#

