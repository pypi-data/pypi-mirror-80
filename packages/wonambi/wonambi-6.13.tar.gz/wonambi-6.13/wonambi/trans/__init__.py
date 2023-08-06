"""Package to transform the Data.

The modules in this package are classes (and maybe functions) that transform
the data into data again (all the classes defined in datatype.py). Do not
use this package to transform to other classes. If you want to transform to
basic elements, use the package "detect" for example.

"""
from .filter import filter_, convolve
from .select import (select, resample, get_times, _select_channels, fetch,
                     Segments)
from .frequency import frequency, timefrequency, band_power
from .merge import concatenate
from .math import math, get_descriptives
from .montage import montage, create_virtual_channel
from .peaks import peaks
from .reject import rejectbadchan, remove_artf_evts
from .analyze import export_freq, export_freq_band
from .baseline import apply_baseline
