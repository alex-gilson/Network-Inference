from brian2 import *

start_scope()


seed = 1
N = 20
sparsity=0.1
# set the default seed
devices.device.seed(seed)

# suppress warnings
BrianLogger.suppress_hierarchy('brian2.codegen')

firings=[]
indices=[]

tau=1*ms

eqs= '''
dv/dt = (0.04*v*v + 5*v + 140 - u + I + stimulation)/tau : 1
du/dt = (a*(b*v-u))/tau : 1
I = 12*randn() : 1 (constant over dt)
a:1
b:1
c:1
d:1
stimulation:1
'''

threshold='v>30'

reset='''
v=c
u=u+d
'''
# Initialise the Neuron Group and set the Parameters
G = NeuronGroup(1,eqs,threshold=threshold,reset=reset,method='euler')
M = StateMonitor(G, 'v', record=0)
G.a = 0.1
G.b = 0.2
G.c = '-65'
G.d = '2'

# Define the connection values and the conditions
S = Synapses(G, G, 'w:1', on_pre='v_post += w')
S.connect(condition='i!=j', p=sparsity)
S.w='30*rand()'

statemon = StateMonitor(G, 'v', record=0)
spikemon = SpikeMonitor(G)

run(500*ms)
plot(statemon.t/ms, statemon.v[0])
# for t in spikemon.t:
#     axvline(t/ms, ls='--', c='blue', lw=3)
# axhline(0.8, ls=':', c='blue', lw=3)
xlabel('Time (ms)')
ylabel('Membrane potential (mv)')
grid()
title('Fast Spiking neuron with constant imput = 5')
print("Spike times: %s" % spikemon.t[:])
show()
