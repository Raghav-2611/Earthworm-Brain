from brian2 import *
import csv

neuron_names = []
with open("data/neurons.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        neuron_names.append(row[0])

N = len(neuron_names)
neuron_index = {name: i for i, name in enumerate(neuron_names)}

connections = []
with open("data/connections.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        pre = neuron_index[row[0]]
        post = neuron_index[row[1]]
        weight = float(row[2]) * mV  
        connections.append((pre, post, weight))

tau = 10*ms
tau_syn = 5*ms
v_rest = -65*mV
v_thresh = -50*mV
v_reset = -65*mV

eqs = '''
dv/dt = (v_rest - v + I_syn) / tau : volt
dI_syn/dt = -I_syn / tau_syn : volt
'''

neurons = NeuronGroup(N, eqs, threshold='v > v_thresh', reset='v = v_reset', method='exact')
neurons.v = v_rest

S = Synapses(neurons, neurons, 'w : volt', on_pre='I_syn += w')

for pre, post, weight in connections:
    S.connect(i=pre, j=post)
    S.w[pre, post] = weight

stim_indices = [neuron_index[name] for name in neuron_names[:5]]
neurons.I_syn[stim_indices] = 2.5 * mV

spike_mon = SpikeMonitor(neurons)

run(500 * ms)

print(f"\nTotal spikes recorded: {sum(spike_mon.count)}")
print("Neurons that spiked at least once:")
for i, count in enumerate(spike_mon.count):
    if count > 0:
        print(f" - {neuron_names[i]}: {count} spikes")
