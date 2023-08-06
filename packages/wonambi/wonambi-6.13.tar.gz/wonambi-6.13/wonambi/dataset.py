"""Module has information about the datasets, not data.

"""
from datetime import timedelta, datetime
from math import ceil
from logging import getLogger
from pathlib import Path

from numpy import arange, asarray, concatenate, empty, int64, zeros

from .ioeeg import (Abf,
                    Edf,
                    Ktlx,
                    BlackRock,
                    EgiMff,
                    EEGLAB,
                    FieldTrip,
                    BrainVision,
                    Moberg,
                    Wonambi,
                    Micromed,
                    BCI2000,
                    OpenEphys,
                    Text,
                    BIDS,
                    LyonRRI,
                    )
from .ioeeg.bci2000 import _read_header_length
from .datatype import ChanTime
from .utils import UnrecognizedFormat


lg = getLogger('wonambi')


def _convert_time_to_sample(abs_time, dataset):
    """Convert absolute time into samples.

    Parameters
    ----------
    abs_time : dat
        if it's int or float, it's assumed it's s;
        if it's timedelta, it's assumed from the start of the recording;
        if it's datetime, it's assumed it's absolute time.
    dataset : instance of wonambi.Dataset
        dataset to get sampling frequency and start time

    Returns
    -------
    int
        sample (from the starting of the recording).
    """
    if isinstance(abs_time, datetime):
        abs_time = abs_time - dataset.header['start_time']

    if not isinstance(abs_time, timedelta):
        try:
            abs_time = timedelta(seconds=float(abs_time))
        except TypeError as err:
            if isinstance(abs_time, int64):
                # timedelta and int64: http://bugs.python.org/issue5476
                abs_time = timedelta(seconds=int(abs_time))
            else:
                raise err

    sample = int(ceil(abs_time.total_seconds() * dataset.header['s_freq']))
    return sample


def detect_format(filename):
    """Detect file format.

    Parameters
    ----------
    filename : str or Path
        name of the filename or directory.

    Returns
    -------
    class used to read the data.

    list : indices of sessions
    """
    sessions = [1, ]  # start counting from 1
    filename = Path(filename)

    if filename.is_dir():
        if list(filename.glob('*.stc')) and list(filename.glob('*.erd')):
            return Ktlx, sessions
        elif (filename / 'patient.info').exists():
            return Moberg, sessions
        elif (filename / 'info.xml').exists():
            return EgiMff, sessions
        elif list(filename.glob('*.openephys')):
            sessions = _count_openephys_sessions(filename)
            return OpenEphys, sessions
        elif list(filename.glob('*.txt')):
            return Text, sessions
        else:
            raise UnrecognizedFormat('Unrecognized format for directory ' +
                                     str(filename))
    else:
        if filename.suffix == '.won':
            return Wonambi, sessions

        if filename.suffix.lower() == '.trc':
            return Micromed, sessions

        if filename.suffix == '.set':
            return EEGLAB, sessions

        if filename.suffix in ['.edf', '.rec']:
            return Edf, sessions

        if filename.suffix == '.abf':
            return Abf, sessions

        if filename.suffix == '.vhdr' or filename.suffix == '.eeg':
            return BrainVision, sessions

        if filename.suffix == '.dat':  # very general
            try:
                _read_header_length(filename)

            except (AttributeError, ValueError):  # there is no HeaderLen
                pass

            else:
                return BCI2000, sessions

        with filename.open('rb') as f:
            file_header = f.read(8)
            if file_header in (b'NEURALCD', b'NEURALSG', b'NEURALEV'):
                return BlackRock, sessions
            elif file_header[:6] == b'MATLAB':  # we might need to read more
                return FieldTrip, sessions

        if filename.suffix.lower() == '.txt':
            with filename.open('rt') as f:
                first_line = f.readline()
                if '.rr' in first_line[-4:]:
                    return LyonRRI, sessions

        else:
            raise UnrecognizedFormat('Unrecognized format for file ' +
                                     str(filename))


class Dataset:
    """Contain specific information and methods, associated with a dataset.

    Parameters
    ----------
    filename : str or Path
        name of the file
    IOClass : class
        one of the classes of wonambi.ioeeg
    bids : bool
        whether you give precedence to the information stored in the accompanying
        files which are in the BIDS format

    Attributes
    ----------
    filename : str
        name of the file
    IOClass : class
        format of the file
    header : dict
        - subj_id : str
            subject identification code
        - start_time : datetime
            start time of the dataset. If it cannot get the start time from the
            header, wonambi reads it from the timestamp of the file
        - s_freq : float
            sampling frequency
        - chan_name : list of str
            list of all the channels
        - n_samples : int
            number of samples in the dataset
        - orig : dict
            additional information taken directly from the header
    dataset : instance of a class which depends on format,
        this requires at least three attributes:
          - filename
          - return_hdr
          - return_dat

    Notes
    -----
    There is a difference between Dataset.filename and Dataset.dataset.filename
    because the former is where the file that you want to read (the argument),
    while the latter is the file that you really read. There might be
    differences, for example, if the argument points to a file within a
    directory, or if the file is mapped to memory.
    """
    def __init__(self, filename, IOClass=None, session=None, bids=False):
        self.filename = Path(filename)

        if bids:
            IOClass = BIDS

        if IOClass is not None:
            self.IOClass = IOClass
        else:
            self.IOClass, sessions = detect_format(filename)

        if self.IOClass in (OpenEphys, ):
            if session is None:
                session = 1
                if len(sessions) > 1:
                    lg.warning(f'Multiple sessions in the dataset, selecting the first one. You can specify the session with "session="')

            lg.debug(f'Reading session {session}')
            self.dataset = self.IOClass(self.filename, session=session)

        else:
            self.dataset = self.IOClass(self.filename)

        output = self.dataset.return_hdr()
        hdr = {}
        hdr['subj_id'] = output[0]
        hdr['start_time'] = output[1]
        if hdr['start_time'] is None:
            hdr['start_time'] = datetime.fromtimestamp(self.filename.stat().st_mtime)
        hdr['s_freq'] = output[2]
        hdr['chan_name'] = output[3]
        hdr['n_samples'] = output[4]
        hdr['orig'] = output[5]
        self.header = hdr

    def read_markers(self, **kwargs):
        """Return the markers. You can add optional arguments that will be
        passed to the method specific for each datafile.
        """
        return self.dataset.return_markers(**kwargs)

    def read_videos(self, begtime=None, endtime=None):
        """Return list of videos with start and end times for a period.

        Parameters
        ----------
        begtime : int or timedelta or datetime or list
            start of the data to read;
            if it's int, it's assumed it's s;
            if it's timedelta, it's assumed from the start of the recording;
            if it's datetime, it's assumed it's absolute time.
            It can also be a list of any of the above type.
        endtime : int or timedelta or datetime
            end of the data to read;
            if it's int, it's assumed it's s;
            if it's timedelta, it's assumed from the start of the recording;
            if it's datetime, it's assumed it's absolute time.
            It can also be a list of any of the above type.

        Returns
        -------
        list of path
            list of absolute paths (as str) to the movie files
        float
            time in s from the beginning of the first movie when the part of
            interest starts
        float
            time in s from the beginning of the last movie when the part of
            interest ends

        Raises
        ------
        OSError
            when there are no video files at all
        IndexError
            when there are video files, but the interval of interest is not in
            the list of files.
        """
        if isinstance(begtime, datetime):
            begtime = begtime - self.header['start_time']
        if isinstance(begtime, timedelta):
            begtime = begtime.total_seconds()
        if isinstance(endtime, datetime):
            endtime = endtime - self.header['start_time']
        if isinstance(endtime, timedelta):
            endtime = endtime.total_seconds()

        videos = self.dataset.return_videos(begtime, endtime)
        """
        try
        except AttributeError:
            lg.debug('This format does not have video')
            videos = None
        """
        return videos

    def read_data(self, chan=None, begtime=None, endtime=None, begsam=None,
                  endsam=None, events=None, pre=1, post=1, s_freq=None):
        """Read the data and creates a ChanTime instance

        Parameters
        ----------
        chan : list of strings
            names of the channels to read
        begtime : int or timedelta or datetime or list
            start of the data to read;
            if it's int or float, it's assumed it's s;
            if it's timedelta, it's assumed from the start of the recording;
            if it's datetime, it's assumed it's absolute time.
            It can also be a list of any of the above type.
        endtime : int or timedelta or datetime
            end of the data to read;
            if it's int or float, it's assumed it's s;
            if it's timedelta, it's assumed from the start of the recording;
            if it's datetime, it's assumed it's absolute time.
            It can also be a list of any of the above type.
        begsam : int
            first sample (this sample will be included)
        endsam : int
            last sample (this sample will NOT be included)
        events : list of int or of timedelta or of datetime
            list of the onset time of the events of interest.
            This option is useful if you want to run a trial-based analysis.
        pre : float
            only when "events" is specified, the amount of data before each
            event to be included (in s). Use a positive number to indicate
            the time before the event.
        post : float
            only when "events" is specified, the amount of data after each
            event to be included (in s).
        s_freq : int
            sampling frequency of the data

        Returns
        -------
        An instance of ChanTime

        Notes
        -----
        begsam and endsam follow Python convention, which starts at zero,
        includes begsam but DOES NOT include endsam.

        If begtime and endtime are a list, the two lists should have the same
        length and the data will be stored in trials.

        If neither begtime or begsam are specified, it starts from the first
        sample. If neither endtime or endsam are specified, it reads until the
        end.

        The time axis will indicate the time in seconds from data.start_time,
        unless you specify "events". In that case, time will run from -"pre" to
        +"post".
        """
        data = ChanTime()
        data.start_time = self.header['start_time']
        data.s_freq = s_freq = s_freq if s_freq else self.header['s_freq']

        if chan is None:
            chan = self.header['chan_name']
        if not (isinstance(chan, list) or isinstance(chan, tuple)):
            raise TypeError('Parameter "chan" should be a list')
        add_ref = False
        if '_REF' in chan:
            add_ref = True
            chan[:] = [x for x in chan if x != '_REF']
        idx_chan = [self.header['chan_name'].index(x) for x in chan]

        if begtime is None and begsam is None:
            begsam = 0
        if endtime is None and endsam is None:
            endsam = self.header['n_samples']

        if events is not None:
            eventssam = self._convert_to_list_with_samples(events)
            presam = int(pre * s_freq)
            postsam = int(post * s_freq)
            begsam = [event - presam for event in eventssam]
            endsam = [event + postsam for event in eventssam]

            event_t = arange(-presam, postsam) / s_freq

        begsam = self._convert_to_list_with_samples(begtime, begsam)
        endsam = self._convert_to_list_with_samples(endtime, endsam)

        if len(begsam) != len(endsam):
            raise ValueError('There should be the same number of start and ' +
                             'end point')
        n_trl = len(begsam)

        data.axis['chan'] = empty(n_trl, dtype='O')
        data.axis['time'] = empty(n_trl, dtype='O')
        data.data = empty(n_trl, dtype='O')

        for i, one_begsam, one_endsam in zip(range(n_trl), begsam, endsam):
            dataset = self.dataset
            lg.debug('begsam {0: 6}, endsam {1: 6}'.format(one_begsam,
                     one_endsam))
            dat = dataset.return_dat(idx_chan, one_begsam, one_endsam)
            chan_in_dat = chan

            if add_ref:
                zero_ref = zeros((1, one_endsam - one_begsam))
                dat = concatenate((dat, zero_ref), axis=0)
                chan_in_dat.append('_REF')

            data.data[i] = dat
            data.axis['chan'][i] = asarray(chan_in_dat, dtype='U')
            if events is not None:
                data.axis['time'][i] = event_t
            else:
                data.axis['time'][i] = arange(one_begsam, one_endsam) / s_freq

        return data

    def _convert_to_list_with_samples(self, times=None, samples=None):
        """Convenience function to convert the input into a list of samples"""
        if times is not None:
            if not isinstance(times, list):
                times = [times]
            samples = []
            for one_time in times:
                samples.append(_convert_time_to_sample(one_time, self))

        if not isinstance(samples, list):
            samples = [samples]

        return samples


def _count_openephys_sessions(filename):
    """Open-ephys can have multiple sessions. We count how many files are in
    the format:
      - Continuous_Data.openephys
      - Continuous_Data_2.openephys
      - Continuous_Data_3.openephys
    """
    sessions = []
    for f in filename.glob('*.openephys'):
        session_number = f.stem[16:]
        if session_number == '':
            sessions.append(1)
        else:
            sessions.append(int(session_number))

    return sorted(sessions)
