'''
Tools for converting JSON files to CSV and vice-versa. Notes on formats:
    - CSV format is "long" format, typically a row for each farm-crop-input
        combination, or each farm-crop-constraint combination.
    - CSV columns are *output* in a predictable order but the order of an
        input CSV file's columns doesn't matter.
'''

import csv
import datetime
import itertools
import json
import numpy as np
import pandas as pd
from dateutil.parser import parse
from typing import Sequence
from collections import OrderedDict

# Map JSON keys to CSV keys; hard-coded exceptions:
#   "id", "name", "source_id", "crop_id", "crop_list" -> "crop",
#   "input_list" -> "input", "constraints" -> "constraint"
#   All members of "parameters" are hard-coded
MAP_FARM_JSON_TO_CSV = OrderedDict({
    'irrigation_mask': 'irrigation_mask',
    'irrigation_eff': 'irrigation_eff',
    # 1 per crop type unless otherwise specified
    'normalization_refs': OrderedDict({
        'reference_et': 'reference_et',
        'reference_land': 'reference_land',
        'reference_prices': 'reference_prices',
        'reference_yields': 'reference_yields',
    }),
    # 1 per crop type unless otherwise specified
    'simulated_states': OrderedDict({
        'shadow_prices': 'shadow_prices', # Exactly 1
        'supply_elasticity_eta': 'supply_elasticity_eta',
        'yield_elasticity_water': 'yield_elasticity_water',
        'yields': 'yields',
        'used_land': 'used_land',
        'used_water': 'used_water',
        'net_revenues': 'net_revenues', # Exactly 1
    }),
    # 1 per crop type unless otherwise specified
    'parameters': OrderedDict({
        'lambdas_land': 'lambdas_land', # 1 per constraint
        'betas': 'betas', # 1 per constraint
        'deltas': 'deltas',
        'mus': 'mus',
        'first_stage_lambda': 'first_stage_lambda', # Exactly 1 (but as a list)
        'sigmas': 'sigmas', # Exactly 1 (but as a list)
    })
})

# Map JSON keys to CSV keys; hard-coded exceptions:
#   "id", "name", "year", "crop_list" -> "crop"
#   "mean_costs" is zip("cost_land", "cost_water")
#   "std_costs" is zip("cost_land_sd", "cost_water_sd")
MAP_OBS_JSON_TO_CSV = OrderedDict({
    'mean_eta': 'supply_elasticity',
    'mean_ybar': 'production',
    'mean_obs_land': 'area_planted',
    'mean_obs_water': 'crop_water_observation',
    'mean_ybar_w': 'yield_elasticity',
    'mean_prices': 'crop_prices',
    'std_eta': 'supply_elasticity_sd',
    'std_ybar': 'production_sd',
    'std_obs_land': 'area_planted_sd',
    'std_obs_water': 'crop_water_observation_sd',
    'std_ybar_w': 'yield_elasticity_sd',
    'std_prices': 'crop_prices_sd',
})

MAP_OBS_CSV_TO_JSON = OrderedDict( # Invert key-item pairs
    ((v, k) for k, v in MAP_OBS_JSON_TO_CSV.items())
)

def farms_csv_to_json(
        input_csv: str, output_json: str = None, sep: str = ',',
        crops: Sequence = None, years: Sequence = None):
    '''
    Converts a Farms CSV to JSON format.

    Parameters
    ----------
    input_csv : str
        File path to the input CSV file
    output_json : str or None
        File path to the output JSON file (Optional)
    sep : str
        Delimiter for input CSV file (Default: ",")
    crops : Sequence or None
        Sequence of crops to include when reading CSV file; if None, read all

    Returns
    -------
    dict
        Python equivalent of JSON data dictionary
    '''
    # TODO Need to fix "parameters" conversion, particularly "betas"
    results = []
    df = pd.read_csv(
        input_csv, sep = sep, dtype = {'id': str},
        index_col = ('id', 'name', 'source_id', 'crop_id', 'crop', 'input'))

    if crops is not None:
        # 4 refers to "crop" index
        df = df[df.index.get_level_values(4).isin(crops)]

    results = {'farms': list()}
    # TODO This may not work in some cases because pandas coerces "id"
    #   index to integer
    for f in list(map(str, df.index.unique(0).values.tolist())):
        data = dict()
        df_farm = df[df.index.get_level_values('id').isin([f])]
        df_farm = df_farm.fillna(0) # Make NaNs zero
        # Iterate over fields enumerated by crop
        data['id'] = str(df_farm.index.unique(0)[0])
        data['name'] = df_farm.index.unique(1)[0]
        data['source_id'] = int(df_farm.index.unique(2)[0])
        data['crop_id'] = df_farm.index.unique(3).tolist()
        data['crop_list'] = df_farm.index.unique(4).tolist()
        data['input_list'] = df_farm.index.unique(5).tolist()
        data['constraints'] = dict([
            (level, series['constraint'].unique().tolist())
            for level, series in df_farm.groupby(level = 5)
        ])
        for j_key, c_key in MAP_FARM_JSON_TO_CSV.items():
            if j_key in ('normalization_refs', 'parameters', 'simulated_states'):
                data[j_key] = dict()
                for j_subkey, c_subkey in c_key.items():
                    if c_subkey in ('shadow_prices', 'net_revenues'):
                        data[j_key][j_subkey] = float(df_farm[c_subkey].values[0])
                    elif c_subkey in ('first_stage_lambda', 'sigmas'):
                        data[j_key][j_subkey] = [
                            float(df_farm[c_subkey].values.tolist()[0])
                        ]
                    elif c_subkey in ('betas', 'lambdas_land'):
                        data[j_key][j_subkey] = [
                            df_farm[c_subkey].groupby(level = 4).get_group(c)\
                                .values.tolist()
                            for c in data['crop_list']
                        ]
                    else:
                        # Values won't be in the right order, so get the
                        #   crop names...
                        c_order = df_farm[c_subkey].groupby(level = 4)\
                            .first().index.tolist()
                        # ...Then use them to sort the values
                        data[j_key][j_subkey] = [
                            df_farm[c_subkey].groupby(level = 4).first()[i]
                            for i in [data['crop_list'].index(c) for c in c_order]
                        ]
            else:
                # Again, values aren't in the right order, so...
                group = df_farm[c_key].groupby(level = 4).first()
                c_order = group.index.tolist()
                data[j_key] = [
                    group.values.tolist()[i]
                    for i in [data['crop_list'].index(c) for c in c_order]
                ]
        results['farms'].append(data.copy())

    if output_json is not None:
        with open(output_json, 'w') as file:
            json.dump(results, file)

    return results


def farms_json_to_csv(input_json, output_csv: str, **kwargs):
    '''
    Converts a Farms.json file or Farms JSON dictionary to an output CSV file.
    Assumes there is a single source_id per farm. Also strong assumptions
    regarding the "constraints" field (inputs).

    Parameters
    ----------
    input_json : str or dict
        File path to the input JSON file or a dictionary that is
        JSON-serializable
    output_csv : str
        File path to the output CSV file
    kwargs : dict
        Additional keyword arguments to csv.writer()
    '''
    if hasattr(input_json, 'upper') and hasattr(input_json, 'lower'):
        with open(input_json, 'r') as file:
            all_farms = json.load(file)
    elif hasattr(input_json, 'keys') and hasattr(input_json, 'values'):
        all_farms = input_json.copy() # It's a dictionary
    else:
        raise NotImplementedError('"input_json" must be a file path or Dictionary')

    header_ids = ('id', 'name', 'source_id',)
    header_crop_ids = ('crop_id', 'crop', 'input', 'constraint')
    # As in, maps to a sequence of values, not another dict
    header_seq = list(filter(
        lambda v: hasattr(v, 'lower'), MAP_FARM_JSON_TO_CSV.values()))
    header = list(header_ids)
    header.extend(header_crop_ids)
    header.extend(header_seq)
    header.extend(MAP_FARM_JSON_TO_CSV['normalization_refs'].values())
    header.extend(MAP_FARM_JSON_TO_CSV['simulated_states'].values())
    header.extend(MAP_FARM_JSON_TO_CSV['parameters'].values())
    # Iterate through Farm x Crop x Constraint/Input (Land, Water)
    with open(output_csv, 'w') as file:
        writer = csv.writer(file, **kwargs)
        writer.writerow(header)
        # Using a loop when iterating rows, comprehensions for any other
        #   iteration; note also that columns added IN ORDER as code
        for farm in all_farms['farms']:
            # Certain dict keys will be re-used for each Crop-Constraint row
            data_ids = [farm[k] for k in header_ids]
            for i, crop in enumerate(farm['crop_list']):
                data_crop_ids = [farm['crop_id'][i], farm['crop_list'][i]]
                for j, input in enumerate(('land', 'water')):
                    data = [input]
                    # TODO Note that constraints currently contains a list
                    data.append(farm['constraints'][input][0])
                    data.extend([
                        farm[k][i] for k in header_seq
                    ])
                    data.extend([
                        farm['normalization_refs'][k][i]
                        for k in MAP_FARM_JSON_TO_CSV['normalization_refs'].keys()
                    ])
                    data.extend([
                        farm['simulated_states'][k][i] if not k in ('shadow_prices', 'net_revenues') else farm['simulated_states'][k]
                        for k in MAP_FARM_JSON_TO_CSV['simulated_states'].keys()
                    ])
                    data.extend([ # These have 1 value per constraint/ input
                        farm['parameters'][k][i][j]
                        for k in ('lambdas_land', 'betas')
                    ])
                    data.extend([ # These have 1 value per crop
                        farm['parameters'][k][i]
                        for k in ('deltas', 'mus')
                    ])
                    data.extend([ # These have exactly 1 value
                        farm['parameters'][k][0] # FIXME Why are these a list?
                        for k in ('first_stage_lambda', 'sigmas')
                    ])
                    # FINALLY
                    writer.writerow((*data_ids, *data_crop_ids, *data))


def observations_csv_to_json(
        input_csv: str, output_json: str = None, sep: str = ',',
        crops: Sequence = None, years: Sequence = None):
    '''
    Converts an Observations CSV to JSON format.

    Parameters
    ----------
    input_csv : str
        File path to the input CSV file
    output_json : str or None
        File path to the output JSON file (Optional)
    sep : str
        Delimiter for input CSV file (Default: ",")
    crops : Sequence or None
        Sequence of crops to include when reading CSV file; if None, read all
    years : Sequence or None
        Sequence of years to include when reading CSV file; if None, read all

    Returns
    -------
    dict
        Python equivalent of JSON data dictionary
    '''
    results = []
    df = pd.read_csv(
        input_csv, sep = sep, dtype = {'id': str},
        index_col = ('id', 'year', 'crop'))

    if crops is not None:
        # 2 refers to "crop" index
        df = df[df.index.get_level_values(2).isin(crops)]

    for id, df_farm in df.groupby(level = (0, 1)):
        data = dict()
        if years is not None:
            if id[1] not in years:
                continue # Skip records for years outside of specified list

        df_farm = df_farm.fillna(0) # Make NaNs zero
        # Get list of crops and year from index level 1 and 2
        data['crop_list'] = list(df_farm.index.get_level_values(2))
        data['year'] = id[1].tolist()
        data['id'] = str(id[0].tolist())
        data['name'] = df_farm['name'].values[0]
        data['mean_costs'] = list(zip(list(df_farm['cost_land']), list(df_farm['cost_water'])))
        data['std_costs'] = list(zip(list(df_farm['cost_land_sd']), list(df_farm['cost_water_sd'])))
        for c_key, j_key in MAP_OBS_CSV_TO_JSON.items():
            data[j_key] = list(df_farm[c_key])
        results.append(data.copy())

    if output_json is not None:
        with open(output_json, 'w') as file:
            json.dump(results, file)

    return results


def observations_json_to_csv(input_json, output_csv: str, **kwargs):
    '''
    Converts an Observations JSON file to a CSV file. The observations file
    describes the observed land allocations and costs (mean and standard
    deviation) for each crop type in a given year.

    Parameters
    ----------
    input_json : str or Sequence
        File path to the input JSON file or a dictionary that is
        JSON-serializable
    output_csv : str
        File path to the output CSV file
    kwargs : dict
        Additional keyword arguments to csv.writer()
    '''
    if hasattr(input_json, 'upper') and hasattr(input_json, 'lower'):
        with open(input_json, 'r') as file:
            observations = json.load(file)
    elif hasattr(input_json, 'count') and hasattr(input_json, 'index'):
        observations = list(input_json) # It's a dictionary
    else:
        raise NotImplementedError('"input_json" must be a file path or Sequence')

    header_costs = ('cost_land', 'cost_land_sd', 'cost_water', 'cost_water_sd')
    header_ids = ('id', 'name', 'year')
    header = list(header_ids)
    header.append('crop')
    header.extend(list(MAP_OBS_JSON_TO_CSV.values()))
    header.extend(header_costs)
    # Iterate through Farm x Crop x Constraint (Land, Water)
    with open(output_csv, 'w') as file:
        writer = csv.writer(file, **kwargs)
        writer.writerow(header)
        for obs in observations:
            # Certain dict keys will be re-used for each Crop-Constraint row
            identifiers = [obs[k] for k in header_ids]
            for i, crop in enumerate(obs['crop_list']):
                # Get the ith entry (corresponding to current crop) of
                #   each statistic, in expected order
                stats = [obs[k][i] for k in MAP_OBS_JSON_TO_CSV.keys()]
                # Get the jth entry (water or land) of each cost
                costs = [
                    obs[k][i][j] # k is the "key"
                    for j, k in itertools.product(
                        (0, 1), ('mean_costs', 'std_costs'))
                ]
                # TODO If we want to generalize the costs/ constraints
                #   framework, this is where to put an additional loop, over
                #   costs (e.g., for j, cost in enumerate(('land', 'water')))
                writer.writerow((*identifiers, crop, *stats, *costs))


class ModelTimeSeries(object):
    '''
    Handles model time series outputs.
    '''
    def __init__(
            self, conn_matrix: pd.DataFrame, init_date: str,
            fname: str = r'streamflows.json', dt: int = 1):
        '''
        Initializes object with connectivity matrix, the initial date and the
        size of the simulation time step (defaults to 1 day).

        Parameters
        ----------

        conn_matrix : pandas.DataFrame
            Connectivity matrix of stream network, pandas dataframe
        init_date : str
            Date of first time step, string
        name : str
            Output filename
        dt : int
            Time step size, days
        '''
        self.conn_matrix = conn_matrix
        self.init_date = parse(init_date)
        self.fname = fname
        self.dt = datetime.timedelta(days = dt)

    def write_json(self, data: list, units: str = "m3/s"):
        """
        Writes list of model outputs at each node as a JSON file.

        Parameters
        ----------

        data : list
            List of lists of numpy array with flows
        units : str
            Description of the units to output

        Returns
        -------
        dict
            JSON dictionary in the format described above
        """
        lst_nodes = []
        data = np.array(data).T
        for row, nodeid in enumerate(self.conn_matrix.index.values):
            node = {"id": int(nodeid.tolist())}
            node["units"] = str(units)
            node["dates"] = \
                [{"date": (self.init_date + ts * self.dt).strftime("%Y/%m/%d"),
                  "flow": d.tolist()} for ts, d in enumerate(data[row])]

            lst_nodes.append(node)

        dict_nodes = {"nodes": lst_nodes}

        with open(self.fname, 'w') as buff:
            json.dump(dict_nodes, buff, indent=4)

        return dict_nodes


if __name__ == '__main__':
    import fire
    fire.Fire(farms_csv_to_json)
