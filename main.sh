# !/usr/local/bin/bash

seed="$1"
num_nodes="$2"
sparsity="$3"
simulation_duration="$4"
networkFileName="$5"
firingsFileName="$6"
indicesFileName="$7"
resultsFileName="$8"
inferredNetworkFileName="$9"
diffusion_type="${10}"
horizon="${11}"
num_processors="${12}"
stimulation_type="${13}"
I_var="${14}"
infer_network="${15}"
cascadesFileName="${16}"
aBadFileName="${17}"
aPotentialFileName="${18}"
numCascadesFileName="${19}"
cascadeOption="${20}"
repeat="${21}"
aHatFileName="${22}"
timeFileName="${23}"
numFiringsFileName="${24}"

# Activate virtual environment
. py27env/bin/activate

# It's a simulated network
if [ ! -f $networkFileName ] || [ ! -f $firingsFileName ] || [ ! -f $indicesFileName ]
then
	python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName $I_var $stimulation_type

else
	echo -e "Found Brian Simulator files"
fi

if (($infer_network == 1))

then

	if [ ! -f $aBadFileName ] || [ ! -f $aPotentialFileName ] || [ ! -f $cascadesFileName ] || [ ! -f $numCascadesFileName ] || (($repeat == 1))
	then

		echo -e "Generating cascades..."

		python generate_cascades.py $num_nodes $indicesFileName $firingsFileName $diffusion_type $horizon $simulation_duration $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $cascadeOption $numFiringsFileName 0 

	else
		echo -e Found cascade files
	fi

	# Get current time and store it into a pickle file
	# python initial_time.py $timeFileName

 	echo -e "Computing Netrate..." 

 	python parallelize_cvx.py $num_processors $num_nodes $horizon $diffusion_type $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $aHatFileName $numFiringsFileName 0 

 	echo -e "Processing results..."

 	python compare_networks.py 1 $aHatFileName $resultsFileName $seed $num_nodes $sparsity $networkFileName $firingsFileName $indicesFileName $inferredNetworkFileName $horizon $diffusion_type $stimulation_type $num_processors $timeFileName $cascadeOption

 	rm $timeFileName 

 	echo "Results are available at '$resultsFileName'"

fi

