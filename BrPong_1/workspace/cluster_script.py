import random
import buildNetwork
import basicRunDORA
import pdb
import numpy as np
import seaborn as sns
NUM_ANALOGS = 4
N_COMPONENTS = 10

parameters = {'asDORA': True, 'gamma': 0.3,
              'delta': 0.05, 'eta': 0.9,
              'HebbBias': 0.5,'bias_retrieval_analogs': True, 'use_relative_act': True,
              #'run_order': ['cdr', 'selectTokens', 'r', 'wp', 'm', 'p', 's', 'f', 'c'],
              'run_order': ['cdr', 'selectTokens', 'r', 'm','c'],
              'run_cyles': 100, 'write_on_iteration': 100, 'firingOrderRule': 'in_order',
              'dim_list':[],
              'strategic_mapping': True, 'ignore_object_semantics': False,
              'ignore_memory_semantics': True, 'mag_decimal_precision': 0,
              'exemplar_memory': False, 'recent_analog_bias': True,
              'lateral_input_level': 1, 'screen_width': 1200, 'screen_height': 700,
              'doGUI': False, 'testing': True, 'GUI_update_rate': 50, 'starting_iteration': 0,
              'tokenize': False, 'ho_sem_act_flow': 0, 'remove_uncompressed': False, 'remove_compressed': False,
              'num_choose':10,'one_to_one':True,'max_norm':True, 'filename':'karthikeya/test_sim_custom-cbow-7-empty_pred.py',
             'len_regularisation':1, 'count_by_RBs':True, 'parent_bias':0.1, 'order_activation_bias':0.5}

def init_network(parameters):
    reload(buildNetwork)
    reload(basicRunDORA)
    fileName = parameters['filename']
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
    network = basicRunDORA.runDORA(memory, parameters)
    memory = basicRunDORA.update_memory_with_levels(memory)
    # run cycles
    # initialise mapping adjacency matrix:
    mapping_adj = np.zeros((len(network.memory.Ps), len(network.memory.Ps)))
    return [network, memory, mapping_adj]

def vis_mappings(mapping_mat, prop_names):
    sns_heatmap = sns.heatmap(mapping_mat, linewidth=0.5,xticklabels=prop_names, yticklabels=prop_names)
    fig = sns_heatmap.get_figure()
    return

def get_metrics(mapping_mat):
    # mapping_mat contains the predicted mappings
    target_mat = np.zeros(mapping_mat.shape)
    per_analog = mapping_mat.shape[0]/NUM_ANALOGS
    for row in range(target_mat.shape[0]):
        target_indices = [(idx*per_analog + row%per_analog) for idx in range(NUM_ANALOGS)] # fill the target mapping indices
        target_indices.pop(target_indices.index(row))
        target_mat[row,target_indices] = 1
    # target_mat contains the true mappings in boolean values
    # Get True Positives (TP)
    true_positives = sum(sum(mapping_mat * target_mat))
    # False Positives (FP)
    false_positives =  sum(np.sum(mapping_mat * abs(target_mat-1), axis=0))# gives all those non-zero mappings at the wrong place.
    # False Negatives (FN) giving zero mapping when it should actually be non zero
    false_negatives = sum(np.sum(mapping_mat * abs(target_mat-1), axis=1))
    precision = true_positives/(true_positives + false_positives)
    recall = true_positives/(true_positives + false_negatives)
    f_score = (2 * precision * recall) / (precision + recall)
    return precision, recall, f_score

def run_dora(parameters):
    network, memory, mapping_adj = init_network(parameters)
    precisions, recalls, fscores = [], [], []
    for cycle in range(parameters['run_cyles']):
        print('\n\n************************* Cycle: ' + str(cycle + 1))
        # pdb.set_trace()
        # clear driver and recipient
        network.memory = basicRunDORA.clearDriverSet(network.memory)
        network.memory = basicRunDORA.clearRecipientSet(network.memory)
        # choose random analog from memory
        analog = random.choice(network.memory.analogs)  # currently only one analog
        # choose random propositions from memory

        # put the analog in the driver
        analog_num = network.memory.analogs.index(analog)
        network.memory = basicRunDORA.add_tokens_to_set(network.memory, analog_num, 'analog', 'driver')
        # retrieve analogs similar to one in the driver from LTM
        network.memory = basicRunDORA.findDriverRecipient(network.memory)
        network.do_retrieval()
        network.memory = basicRunDORA.findDriverRecipient(network.memory)

        # print('In driver : ' + network.memory.driver.Ps[0].name[1])
        # if len(network.memory.recipient.Ps) > 0:
        #    print('In recipient : ' + network.memory.recipient.Ps[0].name[1])
        #    if network.memory.recipient.Ps[0].name[1] == '3':
        #        network.do_map()
        #        print('\n\nMappings:\n')
        #        basicRunDORA.DORA_GUI.term_map_display(network.memory, only_Ps=True, only_max=False)

        if len(network.memory.recipient.Ps) > 0:
            print
            'retrieval successful'
            # map the analogs in driver and recipient
            network.do_map()
        # display ALL mappings
        # display mappings
        print('\n\nMappings:\n')
        basicRunDORA.DORA_GUI.term_map_display(network.memory, only_Ps=False, only_max=False)
        # store all mappings :
        for myP in network.memory.driver.Ps:
            for mapping in myP.mappingConnections:
                map_weight = mapping.weight
                map_unit = mapping.recipientToken
                mapping_adj[network.memory.Ps.index(myP), network.memory.Ps.index(map_unit)] += map_weight
        # append rmse to list to keep track of RMSE evolution
        temp_mapping_adj = mapping_adj
        for ind in range(temp_mapping_adj.shape[0]):
            if sum(temp_mapping_adj[ind, :]) > 0:
                temp_mapping_adj[ind, :] = temp_mapping_adj[ind, :] / sum(temp_mapping_adj[ind, :])
        prec, rec, fsc = get_metrics(temp_mapping_adj)
        precisions.append(prec)
        recalls.append(rec)
        fscores.append(fsc)

    # normalise mappings
    for ind in range(mapping_adj.shape[0]):
        if sum(mapping_adj[ind, :]) > 0:
            mapping_adj[ind, :] = mapping_adj[ind, :] / sum(mapping_adj[ind, :])
    return precisions, recalls, fscores, mapping_adj

if __name__ == '__main__':
    run_dora(parameters)