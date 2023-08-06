import json
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Sequence

def suppress_warnings(func):
    'Decorator to suppress warnings'
    def inner(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)
    return inner


class EnsembleResults(object):
    def __init__(self, fn_info_json):

        with open(fn_info_json) as js:
            self.dc_info = json.load(js)

        try:
            self.xi = self.dc_info['xi']
            self.name = self.dc_info['name']
            self.id = self.dc_info['id']
            self.ens_size = self.dc_info['ensemble size']
            self.fn_inn = self.dc_info['innovation']
            self.fn_post = self.dc_info['posterior parameters']
            self.zeta = self.dc_info['zeta']
        except:
            pass

    def load_ensemble(self, header=[0, 1, 2], innovation=False):
        '''return a pandas dataframe with parameter or innovation ensemble'''
        fn = self.fn_post
        if innovation:
            fn = self.fn_inn

        df = pd.read_csv(fn, header=header, index_col=0)

        return df

    def get_percentiles(self, df):
        '''
        Returns the average, 5th, 25th, 75th and 95th percentiles of each
        assimilation cycle of the ensemble

        Parameters
        ----------
        df : pandas.DataFrame
            Ensemble dataframe

        Returns
        -------
        tuple
            Five (5) pandas.Series instances for mean, q5, q25, q75, q95
        '''

        mean = df.median(axis=0)
        q5 = df.quantile(0.05, axis=0)
        q25 = df.quantile(0.25, axis=0)
        q40 = df.quantile(0.40, axis=0)
        q60 = df.quantile(0.60, axis=0)
        q75 = df.quantile(0.75, axis=0)
        q95 = df.quantile(0.95, axis=0)

        return (mean, q5, q25, q40, q60, q75, q95)

    def get_assim_cycles(self, df):
        return df.columns.get_level_values(0).unique()

    def get_parameter_names(self, df):
        return df.columns.levels[1]

    def get_crop_names(self, df):
        return df.columns.levels[2]

    @suppress_warnings
    def plot_parameter_ensemble(
            self, innovation = False, crop_list = None, param_list = None,
            show = True, figsize = None, **kwargs):
        '''
        '''

        df = self.load_ensemble(innovation = innovation)
        if crop_list is None:
            crop_list = list(self.get_crop_names(df))
            crop_list.remove('A')
        if param_list is None:
            param_list = self.get_parameter_names(df).to_list()

        # Append the special crop that holds farm_scale lambda
        # crop_list.append('A')
        mean, q5, q25, q40, q60, q75, q95 = self.get_percentiles(df)
        ind = self.get_assim_cycles(df)
        # If the number of time steps is long, re-format and skip every other
        #   label to make the x-axis readable
        if len(ind) >= 15:
            ind_labels = [
                s.replace('ts_', '') if i % 2 != 0 else ''
                for i, s in enumerate(ind)
            ]
        else:
            ind_labels = ind
        crop_list = set([c.rstrip('_1').rstrip('_2') for c in crop_list])
        time_label = df.columns.unique(0)[0]

        # ax = plt.subplot(len(crop_list), len(param_list), 1)
        if any([x in ['first_stage_lambda', 'inn.fsl'] for x in param_list]):
            nrows, ncols = (len(crop_list) + 1, len(param_list) - 1)
        else:
            nrows, ncols = (len(crop_list), len(param_list))

        fig, ax = plt.subplots(nrows, ncols, squeeze = False, sharex = True)
        axbig = None
        # Prepare bottom plot for fsl if it is in the list of parmaeters
        if any([x in ['first_stage_lambda', 'inn.fsl'] for x in param_list]):
            gs = ax[-1,0].get_gridspec()
            # Remove the underlying axes
            for a in ax[-1, :]:
                a.remove()
            axbig = fig.add_subplot(gs[-1, :])

        for p, paramname in enumerate(param_list):
            c = 0
            for i, cropname in enumerate(df[time_label, paramname].columns):

                # Special case for farm_level first_stage_lambda parameter
                if (paramname == 'first_stage_lambda' or paramname == 'inn.fsl') and len(crop_list) > 1:
                    cropname = 'farm_level' if innovation else 'A'
                    axbig.fill_between(
                        ind, q95.loc[:, paramname, cropname],
                        q5[:, paramname, cropname], edgecolor = 'w',
                        facecolor = 'darkgray', alpha = 0.5, **kwargs)
                    axbig.fill_between(
                        ind, q75[:, paramname, cropname],
                        q25[:, paramname, cropname], edgecolor = 'w',
                        facecolor = 'dimgray', alpha = 0.5, **kwargs)
                    axbig.fill_between(
                        ind, q60[:, paramname, cropname],
                        q40[:, paramname, cropname], edgecolor = 'w',
                        facecolor = 'black', alpha = 0.5, **kwargs)
                    axbig.plot(
                        ind, mean[:, paramname, cropname], c = color,
                        label = paramname, **kwargs)
                    axbig.set_xlim(ind[0], ind[-1])
                    axbig.set_xticklabels(ind_labels)
                    axbig.set_ylabel(
                        cropname, rotation = 90, size = 'large')
                    # ax[c,p].legend()
                    if innovation:
                        axbig.axhline(c = 'k', alpha = 0.5)
                    continue

                if not any([x in cropname for x in crop_list]) and not (cropname == 'A' or cropname == 'farm_level'):
                    continue

                color = 'r'
                if '_' in cropname:
                    if cropname.split('_')[1] == '2':
                        color = 'b'
                        c = c -1

                # ax = plt.subplot(len(crop_list), len(param_list), (c * len(param_list)) + (p+1))
                ax[c,p].fill_between(
                    ind, q95.loc[:, paramname, cropname],
                    q5[:, paramname, cropname], edgecolor = 'w',
                    facecolor = 'darkgray', alpha = 0.5, **kwargs)
                ax[c,p].fill_between(
                    ind, q75[:, paramname, cropname],
                    q25[:, paramname, cropname], edgecolor = 'w',
                    facecolor = 'dimgray', alpha = 0.5, **kwargs)
                ax[c, p].fill_between(
                    ind, q60[:, paramname, cropname],
                    q40[:, paramname, cropname], edgecolor = 'w',
                    facecolor = 'black', alpha = 0.5, **kwargs)
                ax[c,p].plot(
                    ind, mean[:, paramname, cropname], c = color,
                    label = paramname, **kwargs)
                ax[c,p].set_ylabel(cropname, rotation=90, size='large')
                ax[c,p].set_xlim(ind[0], ind[-1])
                ax[c,p].set_xticklabels(ind_labels)
                # ax[c,p].legend()
                if innovation:
                    ax[c,p].axhline(c='k', alpha=0.5)
                c += 1

        if figsize is not None:
            fig.set_figwidth(figsize[0])
            fig.set_figheight(figsize[1])

        # if fname is not None:
        if show:
            plt.tight_layout()
            plt.show()
        return (fig, ax, axbig)

    def plot_simulation_ensemble(
            self, fn_sim_ens: str, state_list: Sequence = None,
            crop_list: Sequence = None, figsize: Sequence = None,
            wrap: bool = False, savefig: str = None, **kwargs):
        '''
        Parameters
        ----------
        fn_sim_ens : str
            File path to the simulation ensemble HDF5 file
        state_list : list or tuple or None
            Sequence of str indicating which state variables to plot; if
            None, prints all state variables (Default: None)
        crop_list : list or tuple or None
            Sequence of str indicating which crops to plot; if None,
            prints all crops (Default: None)
        figsize : list or tuple or None
            Two-element sequence of the width and height, in inches of the
            figure, i.e., [<width>, <height>]
        wrap : bool
            If True, wrap the plots of multiple crops for a single state (or
            multiple state variables for a single crop) into a grid
            (Default: False)
        savefig : str or None
            If not None, save the plot to the output PDF file path
        **kwargs
            Other keyword arguments to matplotlib.pyplot.hist()
        '''
        df = pd.read_hdf(fn_sim_ens)
        # Show only certain state variables, certain crops
        state_list = df.columns.tolist() if state_list is None else state_list
        crop_list = df.index.levels[1].tolist() if crop_list is None else crop_list
        # Determine how many rows would be needed to wrap crops or wrap states
        if wrap and len(crop_list) > 1:
            assert len(state_list) == 1,\
            '''
            Cannot wrap crops when more than state variable is requested
            (state_list = None plots ALL state variables)
            '''
            nrow = int(np.ceil(len(crop_list) / 2))
            wrapping = crop_list
        elif wrap and len(state_list) > 1:
            assert len(crop_list) == 1,\
            '''
            Cannot wrap state variables when more than one crop is requested
            (crop_list = None plots ALL crop types)
            '''
            nrow = int(np.ceil(len(state_list) / 2))
            wrapping = state_list

        # Optionally wrap the plots of multiple crops (for a single state
        #   variable) or of multiple state variables (for a single crop),
        #   instead of putting the plots in a single row or single column
        if wrap:
            fig, axes = plt.subplots(nrow, 2)
            # If an odd number of plots, delete the last (empty) subplot
            if len(wrapping) % 2 != 0:
                fig.delaxes(axes[nrow - 1, 1])
            i = 0
            for r in range(0, len(axes)):
                for c in range(0, 2):
                    # Again, for odd numbers... Don't index beyond last item
                    if i >= len(wrapping):
                        break
                    if len(state_list) == 1:
                        data = df[state_list[0]].unstack()[crop_list[i]]
                        axes[r,c].hist(data, density=True, **kwargs)
                        axes[r,c].set_xlabel(state_list[0], size = 'large')
                        axes[r,c].set_title(crop_list[i], size = 'large')
                    else:
                        data = df[state_list[i]].unstack()[crop_list[0]]
                        axes[r,c].hist(data, density=True, **kwargs)
                        axes[r,c].set_xlabel(state_list[i], size = 'large')
                        # For a single crop, set the crop name as suptitle
                        if i == len(wrapping) - 1:
                            fig.suptitle(crop_list[0], size = 'large')
                    i += 1
        else:
            # Otherwise, create a Crop x State subplots grid
            counts = (len(crop_list), len(state_list))
            # Make sure we have more rows than columns, as the histograms
            #   should be wider than they are tall
            nrow, ncol = (max(counts), min(counts))
            fig, axes = plt.subplots(nrow, ncol, squeeze=False)
            crop_major = len(crop_list) > len(state_list)
            for state, state_name in enumerate(state_list):
                for crop, crop_name in enumerate(crop_list):
                    r, c = (crop, state) if crop_major else (state, crop)
                    data = df[state_name].unstack()[crop_name]
                    axes[r, c].hist(data, density=True, **kwargs)
                    axes[r, c].set_xlabel(state_name, size = 'large')
                    axes[r, c].set_title(crop_name, size = 'large')

        if figsize is not None:
            fig.set_figwidth(figsize[0])
            fig.set_figheight(figsize[1])

        plt.tight_layout()
        if savefig is not None:
            plt.savefig(savefig)
        plt.show()
