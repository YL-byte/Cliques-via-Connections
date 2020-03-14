from operator import getitem
source = 'Source.txt'
destination = 'Results.txt'

def read_source_file():
    source_file = open(source, 'r')
    source_text = source_file.read()
    source_file.close()
    source_table = parse_text(source_text)
    return source_table

def parse_text(source_text, new_line_char = '\n', new_cell_char = '\t'):
    new_table = []
    cell_value = ''
    current_row = []
    illegal_cell_values = ['',' ',None,'\t','\n']
    for char in source_text:
        #New Row - Reset Cell and Row after append
        if char == new_line_char:
            #Check if new line is legal = Contains only two entities
            current_row.append(cell_value)
            if len(current_row) == 2 and current_row[0] not in illegal_cell_values and current_row[1] not in illegal_cell_values:
                new_table.append(current_row)
            current_row = []
            cell_value = ''

        #New cell - Reset cell after append
        elif char == new_cell_char:
            current_row.append(cell_value)
            cell_value = ''

        #Add the char to current cell value
        else:
            cell_value += char
    #Append last cell to row and last row to table if legal
    if len(current_row) == 2 and current_row[0] not in illegal_cell_values and current_row[1] not in illegal_cell_values:
        current_row.append(cell_value)
        new_table.append(current_row)
    return new_table

def create_index(pairs_table):
    index_to_entity = {}
    entity_to_index = {}
    index_counter = 0
    pairs_table_index = []

    #Create index for each entity
    for pair in pairs_table:
        index_pair = []
        for entity in pair:
            #Create index for entity and raise counter
            if entity not in entity_to_index:
                index_to_entity[index_counter] = entity
                entity_to_index[entity] = index_counter
                index_counter += 1
        #Add index equiv to entity in current pair
            index_pair.append(entity_to_index[entity])
        #Add pair as indexed pair to pairs_table_index
        pairs_table_index.append(index_pair)

    #Index table will host all connections of an entity in the index; For example entity 0's connections will be set in element 0 in the table
    index_table = []
    for i in range (0, len(index_to_entity)):
        index_table.append([])

    for pair in sorted(pairs_table_index):
        entity_a = pair[0]
        entity_b = pair[1]
        if entity_b not in index_table[entity_a]:
            index_table[entity_a].append(entity_b)
        if entity_a not in index_table[entity_b]:
            index_table[entity_b].append(entity_a)
    return index_table, pairs_table_index, index_to_entity, entity_to_index

def create_cliques(index_table, pairs_table_index):
    cliques = []
    for pair in pairs_table_index:
        clique = sorted(pair)
        for checked_entity_index in range (0, len(index_table)):
            #Checked entity must be different from entities in the pair
            if checked_entity_index not in clique:
                #Check if all entities in the current clique are connected to the checked entity:
                to_append = True #Changes into false if checked entity is not connected to at list one of the entities in clique
                for entity in clique:
                    if entity not in index_table[checked_entity_index]:
                        to_append = False
                if to_append == True:
                    clique.append(checked_entity_index)
                    #Check if trio is not in cliques_of_threes
        if clique != sorted(pair) and sorted(clique) not in cliques:
            cliques.append(sorted(clique))
    return cliques

def is_small_clique_in_large_clique(small, large):
    is_true = True
    for entity in small:
        if entity not in large:
            is_true = False
    return is_true

def write_results_to_file(cliques, index_to_entity):
    results_file = open(destination, 'w')
    results_file.write('Group Index\t')
    results_file.write('Num Of Entities\t')
    results_file.write('Entity')
    results_file.write('\n')
    group_index = 1
    for clique in cliques:
        for entity in clique:
            results_file.write(str(group_index) + '\t')
            results_file.write(str(len(clique)) + '\t')
            results_file.write(index_to_entity[entity] + '\n')
#        results_file.write('\n')
        group_index += 1
    results_file.close()


#Pairs Table hosts the pairs; index_table hosts each entitiy's index and entities he is related to
print ('Processing\n')
pairs_table = read_source_file()
print ('Indexing Table\n')
index_table, pairs_table_index, index_to_entity, entity_to_index = create_index(pairs_table)
print ('Creating Cliques\n')
cliques = create_cliques(index_table, pairs_table_index)
cliques = sorted(cliques, key=len, reverse=True)
print ('Writing To File\n')
write_results_to_file(cliques, index_to_entity)
print ('Done')
