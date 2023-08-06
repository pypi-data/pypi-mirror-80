'''
Includes convenience functions for generating Farm, Observation, and Scenario
data dictionary templates.
'''

import numpy as np
import warnings

def generate_farm(n_crops: int, wrap: bool = True):
    '''
    Generates a farm data dictionary template according to the Farms schema;
    users will need to fill in actual data values. For the meanings of the
    "parameters" terms, see the publication Maneta et al. (2020), Env. Model.
    and Softw., linked in the README.

    Parameters
    ----------
    n_crops : int
        The number of crop types
    wrap : bool
        True to wrap the farm template in a within a "farms" list, i.e.,
        {"farms": []} which is the required format (Default: True)

    Returns
    -------
    dict
    '''
    tpl = {
        'id': '000000',
        'name': 'Farm name',
        'source_id': -1,
        'crop_list': ['Crop name'] * n_crops,
        'input_list': ['land', 'water'],
        'simulated_states': {
            'shadow_prices': 0,
            'net_revenues': -1,
        },
        'parameters': {
            'betas': [[-1,  -1] for i in range(0, n_crops)],
            'deltas': [-1] * n_crops,
            'first_stage_lambda': [-1],
            'lambdas_land': [[-1,  -1] for i in range(0, n_crops)],
            'mus': [-1] * n_crops,
            'sigmas': [-1],
        },
        'normalization_refs': dict((
            ('reference_%s' % k, [-1] * n_crops) for k in (
                'yields', 'et', 'land', 'prices'
            )
        )),
        'constraints': {
            'water': [-1],
            'land': [-1]
        }
    }
    # Field with an N-element list for N crop types
    tpl.update(dict((
        (k, [-1] * n_crops) for k in (
            'irrigation_eff', 'irrigation_mask', 'crop_id',
        )
    )))
    tpl['simulated_states'].update(dict((
        (k, [-1] * n_crops) for k in (
            'yields', 'used_land', 'used_water', 'supply_elasticity_eta',
            'yeild_elasticity_water'
        )
    )))
    if wrap:
        return {'farms': [tpl]}
    return tpl


def generate_observation(n_crops: int, n_constraints: int = 2):
    '''
    Generates a farm data dictionary template according to the Farms schema;
    users will need to fill in actual data values. For the meanings of the
    terms, see the publication Maneta et al. (2020), Env. Model. and Softw.,
    linked in the README.

    Parameters
    ----------
    n_crops : int
        The number of crop types
    n_constraints : int
        Number of constraints (Default: 2), defaults to two constraints:
        land and water; this should probably NEVER be changed
    '''
    tpl = {
        'id': "00000",
        'name': 'Farm name',
        'year': 1970,
        'crop_list': ['Crop name'] * n_crops
    }
    # Field with an N-element list for N crop types
    tpl.update(dict((
        (k, [-1] * n_crops) for k in (
            'mean_eta', 'std_eta', 'mean_obs_land', 'std_obs_land',
            'mean_obs_water', 'std_obs_water', 'mean_prices', 'std_prices',
            'mean_ybar', 'std_ybar', 'mean_ybar_w', 'std_ybar_w'
        )
    )))
    # Fields with an M-element list of M constraints for each of N crop types
    tpl.update(dict((
        (k, [[-1] * n_constraints] * n_crops) for k in (
            'mean_costs', 'std_costs'
        )
    )))
    return tpl


def generate_scenario(
        n_crops: int, n_constraints: int = 2, obs: dict = None,
        year: int = None):
    '''
    Generates a scenario data dictionary template according to the Scenarios
    schema; users will need to fill in actual data values. If an Observation
    data dictionary is supplied to the `obs` argument, it should contain *all*
    of the required keys in the Observations schema.

    Parameters
    ----------
    n_crops : int
        The number of crop types
    n_constraints : int
        Number of constraints (Default: 2), defaults to two constraints:
        land and water; this should probably NEVER be changed
    obs : dict or None
        Observation data dictionary, i.e., an element of an Observations.json
        data structure (Default: None)
    year : int or None
        Year of the scenario (Default: None)

    Returns
    -------
    dict
        A data dictionary
    '''
    tpl = {
        'farm_id': '00000',
        'year': 1970,
        'mean_land_constraint': -1,
        'mean_water_constraint': -1,
        'std_land_constraint': -1,
        'std_water_constraint': -1
    }
    # Field with an N-element list for N crop types
    tpl.update(dict((
        (k, [-1] * n_crops) for k in (
            'mean_evapotranspiration', 'std_evapotranspiration',
            'mean_prices', 'std_prices',
        )
    )))
    # Field with an N-element list of dates for N crop types
    tpl.update(dict((
        (k, ['12/31/2020'] * n_crops) for k in (
            'crop_start_date', 'crop_cover_date', 'crop_end_date'
        )
    )))
    # Fields with an N-element list for N constraints
    tpl.update(dict((
        (k, [-1] * n_constraints) for k in (
            'mean_costs', 'std_costs'
        )
    )))
    if obs is not None:
        tpl.update({
            'farm_id': obs['id'],
            'mean_prices': obs['mean_prices'],
            'mean_costs': obs['mean_costs'],
            # Allow farmers to re-allocate land across crop types
            'mean_land_constraint': np.sum(obs['mean_obs_land']).tolist()
        })
    return tpl


def generate_scenario2(
        n_crops: int, farm: dict, obs: dict, year: int,
        use_natural_et: bool = True, irrigation_efficiency: float = 0.95,
        f_water_constraint: float = 1.0, f_cost_land: float = 1.0,
        f_cost_water: float = 1.0):
    '''
    Generates a scenario data dictionary based on observed farm data. There
    are many ways to generate scenario data. Here, we generate a scenario
    that corresponds to the observations, including observed water allocations
    and observed evapotranspiration (ET). This is tricky, because we have to
    separate water transpired due to irrigated crops from water transpired
    in non-irrigated croplands (what we call "natural" ET, below). NOTE: This
    does not generate keys for the standard deviation of observations, e.g.,
    "std_evapotranspiration"; this is fine for PMP simulation but not for
    simulation with a Kalman Filter.

    Parameters
    ----------
    n_crops : int
        The number of crop types
    farm : dict
        Farm data dictionary (i.e., an element of a Farms.json data structure)
    obs : dict
        Observation data dictionary (i.e., an element of an Observations.json
        data structure)
    year : int
        Year of the scenario
    use_natural_et : bool
        True to calculate "natural" evapotranspiration (ET), or the ET from
        non-irrigated croplands
    irrigation_efficiency : float
        Efficiency of irrigation, a number between 0 (0%) and 1 (100%)
        (Default: 0.95)

    Returns
    -------
    dict
        A data dictionary
    '''
    # First, normalize the ET by the amount of land for each crop type
    natural_et = np.array(obs['mean_obs_water']) / np.array(obs['mean_obs_land']).clip(min = 1e-3)
    if use_natural_et:
        ref_land = farm['normalization_refs']['reference_land']
        irr_mask = farm['irrigation_mask'] # True if the crop is irrigated, False if not
        # Take irriagted crops and provide actual ET of nonirrigated crops
        rot_natural_et = natural_et.copy() * np.array(obs['mean_obs_land']) / ref_land
        # Roll -1 because non irrigated crops happen to be adjacent and after nonirrigated
        rot_natural_et[irr_mask] = (np.roll(natural_et, -1))[irr_mask] * (np.array(obs['mean_obs_land']) / ref_land)[irr_mask]
        natural_et[natural_et > rot_natural_et] = rot_natural_et[natural_et > rot_natural_et]
        # Calculate available irrigation water
        available_water = (
            np.array(obs['mean_obs_water'])[irr_mask] - (natural_et * ref_land)[irr_mask]
        ).sum() * irrigation_efficiency # Assuming, e.g., 95% efficiency in irrigation
        if available_water < 0:
            warnings.warn(
                '"available_water" is less than zero; setting to zero',
                UserWarning)
            available_water = 0
    # Generate a scenario file from the farm object
    tpl = generate_scenario(n_crops, obs = obs, year = year)
    tpl.update({
        'farm_id': obs['id'],
        'year': year,
        'mean_evapotranspiration': natural_et.tolist(),
        'std_evapotranspiration': (natural_et * 0.2).tolist(),
        'mean_prices': obs['mean_prices'],
        'mean_costs': (np.asarray(obs['mean_costs']) * np.array([f_cost_land, f_cost_water])).tolist(),
        'std_prices': obs['std_prices'],
        'std_costs': obs['std_costs'],
        'std_land_constraint': np.sqrt(np.sum(np.asarray(obs['std_obs_land'])**2)).tolist(),
        'std_water_constraint': available_water * 0.2,
        # Allow farmers to re-allocate land across crop types
        'mean_land_constraint': np.sum(obs['mean_obs_land']).tolist(),
        'mean_water_constraint': f_water_constraint * available_water,
    })
    keys = (
        'std_evapotranspiration', 'std_land_constraint', 'std_prices',
        'std_costs', 'std_water_constraint',
    )
    test = [np.any(np.array(tpl[k]) < 0) for k in keys]
    if any(test):
        warnings.warn(
            'Scenario key(s) have value(s) less than zero: %s' % (', '.join(keys[test])) if len(keys[test]) > 1 else keys[test])
    return(tpl)
