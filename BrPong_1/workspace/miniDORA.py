import random
import buildNetwork
import basicRunDORA
import pdb
import numpy as np
import sys

parameters = {'asDORA': False, 'gamma': 0.3, 'delta': 0.1, 'eta': 0.9,
              'HebbBias': 0.5,'bias_retrieval_analogs': True, 'use_relative_act': True,
              #'run_order': ['cdr', 'selectTokens', 'r', 'wp', 'm', 'p', 's', 'f', 'c'],
              'run_order': ['cdr', 'selectTokens', 'r', 'm'],
              'run_cyles': 1, 'write_on_iteration': 100, 'firingOrderRule': 'by_top_random',
              'dim_list':[],
              'strategic_mapping': False, 'ignore_object_semantics': True,
              'ignore_memory_semantics': True, 'mag_decimal_precision': 0,
              'exemplar_memory': False, 'recent_analog_bias': True,
              'lateral_input_level': 1, 'screen_width': 1200, 'screen_height': 700,
              'doGUI': False, 'testing': True, 'GUI_update_rate': 50, 'starting_iteration': 0,
              'tokenize': False, 'ho_sem_act_flow': 0, 'remove_uncompressed': False, 'remove_compressed': False,
              'num_choose':10}

# reading symProps from a file
fileName = 'karthikeya/test_sim_8.py'
f = open(fileName, 'r')
simType = ''
d = {'simType': simType}
f.seek(0)
exec (f.readline())
if simType == 'sym_file':
    symstring = ''
    for line in f:
        symstring += line
    exec(symstring)

# initialise memory
memory = buildNetwork.initializeMemorySet()

# interpret sym file
mysym = buildNetwork.interpretSymfile(symProps)

# build the network
memory = basicRunDORA.dataTypes.memorySet()
memory = buildNetwork.buildTheNetwork(mysym[0], memory)
#pdb.set_trace()
network = basicRunDORA.runDORA(memory, parameters)

# run cycles
# initialise mapping adjacency matrix:
mapping_adj = np.zeros((len(network.memory.Ps), len(network.memory.Ps)))

#recursionlimit = sys.getrecursionlimit()
#print 'recursion limit : ', recursionlimit
#sys.setrecursionlimit(2*recursionlimit)


for cycle in range(parameters['run_cyles']):
    print('\n\n************************* Cycle: ' + str(cycle+1))

    # clear driver and recipient
    network.memory = basicRunDORA.clearDriverSet(network.memory)
    network.memory = basicRunDORA.clearRecipientSet(network.memory)

    # choose random analog from memory
    analog = random.choice(network.memory.analogs) # currently only one analog
    # choose random propositions from memory

    # put the analog in the driver
    analog_num = network.memory.analogs.index(analog)
    network.memory = basicRunDORA.add_tokens_to_set(network.memory, analog_num, 'analog', 'driver')

    network.memory = basicRunDORA.findDriverRecipient(network.memory)

    # retrieve analogs similar to one in the driver from LTM
    network.do_retrieval()

    network.memory = basicRunDORA.findDriverRecipient(network.memory)

    # map the analogs in driver and recipient
    network.do_map()
    # display ALL mappings

    for myP in network.memory.driver.Ps:
        for mapping in myP.mappingConnections:
            map_weight = mapping.weight
            if map_weight > 0:
                map_unit = mapping.recipientToken
                if mapping_adj[network.memory.Ps.index(myP), network.memory.Ps.index(map_unit)] < 0.1:
                    mapping_adj[network.memory.Ps.index(myP), network.memory.Ps.index(map_unit)] = map_weight
                else:
                    mapping_adj[network.memory.Ps.index(myP), network.memory.Ps.index(map_unit)] = (map_weight +
                        mapping_adj[network.memory.Ps.index(myP), network.memory.Ps.index(map_unit)])/2.0 # DIRTY SOLUTION FOR NOW

    # display mappings
    print('\n\nMappings:\n')
    basicRunDORA.DORA_GUI.term_map_display(network.memory, only_Ps=True, only_max=False)

#np.savetxt('karthikeya/mapping_adj_6.npy',mapping_adj)