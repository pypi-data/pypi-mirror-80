"""
Utility functions for binning
"""

import numpy as np
import astropy.units as u
from astropy.table import QTable


def add_overflow_bins(bins, positive=True):
    """
    Add under and overflow bins to a bin array.

    Parameters
    ----------
    bins: np.array or u.Quantity
        Bin edges array
    positive: bool
        If True, the underflow array will start at 0, if not at ``-np.inf``
    """
    lower = 0 if positive else -np.inf
    upper = np.inf

    if hasattr(bins, "unit"):
        lower *= bins.unit
        upper *= bins.unit

    if bins[0] > lower:
        bins = np.append(lower, bins)

    if bins[-1] < upper:
        bins = np.append(bins, upper)

    return bins


@u.quantity_input(e_min=u.TeV, e_max=u.TeV)
def create_bins_per_decade(e_min, e_max, bins_per_decade=5):
    """
    Create a bin array with bins equally spaced in logarithmic energy
    with ``bins_per_decade`` bins per decade.

    Parameters
    ----------
    e_min: u.Quantity[energy]
        Minimum energy, inclusive
    e_max: u.Quantity[energy]
        Maximum energy, exclusive
    n_bins_per_decade: int
        number of bins per decade

    Returns
    -------
    bins: u.Quantity[energy]
        The created bin array, will have units of e_min

    """
    unit = e_min.unit
    log_lower = np.log10(e_min.to_value(unit))
    log_upper = np.log10(e_max.to_value(unit))

    bins = 10 ** np.arange(log_lower, log_upper, 1 / bins_per_decade)
    return u.Quantity(bins, e_min.unit, copy=False)


def calculate_bin_indices(data, bins):
    """
    Calculate bin indices for given data array and bins.
    Underflow will be -1 and overflow len(bins) - 1.
    If the bis already include underflow / overflow bins, e.g.
    `bins[0] = -np.inf` and `bins[-1] = np.inf`, using the result of this
    function will always be a valid index into the resultung histogram.


    Parameters
    ----------
    data: ``~np.ndarray`` or ``~astropy.units.Quantity``
        Array with the data

    bins: ``~np.ndarray`` or ``~astropy.units.Quantity``
        Array or Quantity of bin edges. Must have the same unit as ``data`` if a Quantity.


    Returns
    -------
    bin_index: np.ndarray[int]
        Indices of the histogram bin the values in data belong to
    """

    if hasattr(data, "unit"):
        if not hasattr(bins, "unit"):
            raise TypeError(f"If ``data`` is a Quantity, so must ``bin``, got {bins}")
        unit = data.unit
        data = data.to_value(unit)
        bins = bins.to_value(unit)

    return np.digitize(data, bins) - 1


def create_histogram_table(events, bins, key="reco_energy"):
    """
    Histogram a variable from events data into an astropy table.

    Parameters
    ----------
    events : ``astropy.QTable``
        Astropy Table object containing the reconstructed events information.
    bins: ``~np.ndarray`` or ``~astropy.units.Quantity``
        Array or Quantity of bin edges.
        It must have the same units as ``data`` if a Quantity.
    key : ``string``
        Variable to histogram from the events table.

    Returns
    -------
    hist: ``astropy.QTable``
        Astropy table containg the histogram.
    """
    hist = QTable()
    hist[key + "_low"] = bins[:-1]
    hist[key + "_high"] = bins[1:]
    hist[key + "_center"] = 0.5 * (hist[key + "_low"] + hist[key + "_high"])
    hist["n"], _ = np.histogram(events[key], bins)

    # also calculate weighted number of events
    if "weight" in events.colnames:
        hist["n_weighted"], _ = np.histogram(
            events[key], bins, weights=events["weight"]
        )
    return hist
