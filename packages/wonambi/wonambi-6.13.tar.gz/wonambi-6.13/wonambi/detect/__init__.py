"""Package to detect spindles, ripples, slow waves.
"""
from .spindle import DetectSpindle, merge_close, transform_signal
from .ripple import DetectRipple
from .slowwave import DetectSlowWave
from .arousal import DetectArousal
from .agreement import consensus, match_events
