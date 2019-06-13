
seed="$1"
train_test_split=$2
indicesFileName=$3
firingsFileName=$4
networkFileName=$5
trainIndicesFileName=$6
testIndicesFileName=$7
trainFiringsFileName=$8
testFiringsFileName=$9
resultsFileName=${10}
inferredNetworkFileName=${11}
cascadesFileName=${12}
aBadFileName=${13}
aPotentialFileName=${14}
numCascadesFileName=${15}
aHatFileName=${16}
numFiringsFileName=${17}
diffusion_type=${18}
num_nodes=${19}
sparsity=${20}
horizon=${21}
simulation_duration=${22}
I_var=${23}
cascadeOption=${24}

# Activate virtual environment
. py27env/bin/activate

if [ ! -f $networkFileName ] || [ ! -f $firingsFileName ] || [ ! -f $indicesFileName ]
then
	python izhikevichNetworkSimulation.py $seed $num_nodes $sparsity $simulation_duration $networkFileName $firingsFileName $indicesFileName $I_var

else
	echo -e "Found Brian Simulator files"
fi

python train_test_splitter.py $train_test_split $indicesFileName $firingsFileName $trainIndicesFileName $testIndicesFileName $trainFiringsFileName $testFiringsFileName 

if [ ! -f $aBadFileName ] || [ ! -f $aPotentialFileName ] || [ ! -f $cascadesFileName ] || [ ! -f $numCascadesFileName ]
then

	echo -e "Generating cascades..."

	python generate_cascades.py $num_nodes $trainIndicesFileName $trainFiringsFileName $diffusion_type $horizon $simulation_duration $cascadesFileName $aBadFileName $aPotentialFileName $numCascadesFileName $cascadeOption $numFiringsFileName

else
	echo -e Found cascade files
fi

python spike_estimator.py $testIndicesFileName $testFiringsFileName $networkFileName $num_nodes


