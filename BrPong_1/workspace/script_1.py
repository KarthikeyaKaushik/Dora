import random, json
import buildNetwork
import basicRunDORA
import pdb

# set the parameters. 
parameters = {
    'asDORA': False, 
    'gamma': 0.3, 
    'delta': 0.1, 
    'eta': 0.9, 
    'HebbBias': 0.5, 
    'bias_retrieval_analogs': True, 
    'use_relative_act': True, 
    'run_order': ['cdr', 'selectTokens', 'r', 'wp', 'm', 'p', 'f', 's', 'c'], 
    'run_cyles': 5000, 
    'write_on_iteration': 100, 
    'firingOrderRule': 'random', 
    'strategic_mapping': False,
    'ignore_object_semantics': False, 
    'ignore_memory_semantics': True, 
    'dim_list': [], 
    'exemplar_memory': False, 
    'recent_analog_bias': True, 
    'lateral_input_level': 1,
    'mag_decimal_precision': 0,
    'screen_width': 1200, 'screen_height': 700, 'doGUI': True, 'GUI_update_rate': 10, 'starting_iteration': 0}

f = open('karthikeya/test_sim_4.py', 'r')
f.seek(0)  # to get to the beginning of the file.
exec(f.readline())
if simType == 'sym_file':
    symstring = ''
    for line in f:
        symstring += line
    do_run = True
    try:
        exec symstring
    except:
        do_run = False
        print '\nSorry, you have a badly formated sym file. \nI will return to the MainMenu.'

memory = buildNetwork.initializeMemorySet()
# interpret the sym file.
mysym = buildNetwork.interpretSymfile(symProps)
print 'Sym file loaded!'
# build the network object with memory.
memory = basicRunDORA.dataTypes.memorySet()
memory = buildNetwork.buildTheNetwork(mysym[0], memory)
network = basicRunDORA.runDORA(memory, parameters)


def clear_mem():
    network.memory = basicRunDORA.clearDriverSet(network.memory)
    network.memory = basicRunDORA.clearRecipientSet(network.memory)

clear_mem()
network.memory = basicRunDORA.findDriverRecipient(network.memory)
network.do_retrieval()
network.do_map()



