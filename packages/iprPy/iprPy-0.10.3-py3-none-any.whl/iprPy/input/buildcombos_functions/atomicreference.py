# http://www.numpy.org/
import numpy as np

# https://github.com/usnistgov/atomman
import atomman.lammps as lmp

__all__ = ['atomicreference']

def atomicreference(database, keys, content_dict=None, 
                    record='reference_crystal', elements=None,
                    query=None, **kwargs):
    
    if content_dict is None:
        content_dict = {}

    # Check if potential info is in keys
    if 'potential_file' in keys or 'potential_content' in keys or 'potential_dir' in keys:
        include_potentials = True
        
        # Extract kwargs starting with "potential"
        potential_kwargs = {}
        for key in list(kwargs.keys()):
            if key[:10] == 'potential_':
                potential_kwargs[key[10:]] = kwargs.pop(key)
    else:
        include_potentials = False
    
    # Fetch reference records
    references, reference_df = database.get_records(style=record, return_df=True,
                                                    query=query, **kwargs)
    print(len(reference_df), 'matching atomic references found')
    if len(reference_df) == 0:
        raise ValueError('No matching atomic references found')

    # Initialize inputs keys
    inputs = {}
    for key in keys:
        inputs[key] = []
    
    # Do nothing if no references found
    if len(references) == 0:
        return inputs, content_dict

    # Build with potentials
    if include_potentials:
        
        # Pull out potential get_records parameters
        potential_record = potential_kwargs.pop('record', 'potential_LAMMPS')
        potential_query = potential_kwargs.pop('query', None)
        status = potential_kwargs.pop('status', 'active')
        
        # Set all status value
        if status is 'all':
            status = ['active', 'retracted', 'superseded']

        # Fetch potential records 
        potentials, potential_df = database.get_records(style=potential_record, return_df=True,
                                                        query=potential_query, status=status,
                                                        **potential_kwargs)
        print(len(potential_df), 'matching interatomic potentials found')
        if len(potential_df) == 0:
            raise ValueError('No matching interatomic potentials found')
        
        # Loop over all unique reference element sets
        reference_df['elementstr'] = reference_df.symbols.apply(' '.join)
        for elementstr in np.unique(reference_df.elementstr):
            reference_symbols = elementstr.split()
            
            # Loop over all potentials
            for j in potential_df.index:
                potential = potentials[j]
                potential_series = potential_df.loc[j]
                content_dict[potential.name] = potential.content
                potential_symbols = potential_series.symbols
                potential_elements = potential_series.elements
                
                # Loop over all potential element-symbol sets
                for symbolstr in symbolstrings(reference_symbols, potential_elements, potential_symbols):
                    
                    # Loop over all references with the reference element set
                    for i in reference_df[reference_df.elementstr==elementstr].index:
                        reference = references[i]
                        content_dict[reference.name] = reference.content
                
                        # Loop over input keys
                        for key in keys:
                            if key == 'potential_file':
                                inputs['potential_file'].append(potential.name + '.json')
                            elif key == 'potential_content':
                                inputs['potential_content'].append(f'record {potential.name}')
                            elif key == 'potential_dir':
                                inputs['potential_dir'].append(potential.name)
                            elif key == 'potential_dir_content':
                                inputs['potential_dir_content'].append(f'tar {potential.name}')
                            elif key == 'load_file':
                                inputs['load_file'].append(reference.name+'.json')
                            elif key == 'load_content':
                                inputs['load_content'].append(f'record {reference.name}')
                            elif key == 'load_style':
                                inputs['load_style'].append('system_model')
                            elif key == 'family':
                                inputs['family'].append(reference.name)
                            elif key == 'symbols':
                                if elementstr == symbolstr:
                                    inputs['symbols'].append('')
                                else:
                                    inputs['symbols'].append(symbolstr)
                            else:
                                inputs[key].append('')
    
    # Build without potentials
    else:
        # Loop over all references
        for i in reference_df.index:
            reference = references[i]
            content_dict[reference.name] = reference.content
            
            # Loop over input keys
            for key in keys:
                if key == 'load_file':
                    inputs['load_file'].append(reference.name+'.json')
                elif key == 'load_content':
                    inputs['load_content'].append(f'record {reference.name}')
                elif key == 'load_style':
                    inputs['load_style'].append('system_model')
                elif key == 'family':
                    inputs['family'].append(reference.name)
                else:
                    inputs[key].append('')
    
    return inputs, content_dict

def symbolstrings(reference_symbols, potential_elements, potential_symbols):
    
    reference_symbol = reference_symbols[0]
    matches = np.where(np.asarray(potential_elements, dtype=str) == str(reference_symbol))[0]
    for match in matches:
        pot_symbol = potential_symbols[match]
        if len(reference_symbols) == 1:
            yield pot_symbol
        else:
            for child in symbolstrings(reference_symbols[1:], potential_elements, potential_symbols):
                yield pot_symbol + ' ' + child      