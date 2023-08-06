import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    '''
    Encodes numpy numeric data types correctly for JSON serialization. See:
        https://stackoverflow.com/a/57915246/2343309
    '''
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)
