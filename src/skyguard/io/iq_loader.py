"""Load IQ sample data from various file formats."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class IQRecording:
    """Container for IQ recording data and metadata.

    Attributes:
        samples: Complex-valued numpy array of IQ samples.
        sample_rate: Sample rate in Hz (e.g. 2_400_000 for 2.4 MHz).
        center_freq: Center frequency in Hz that the SDR was tuned to.
        source: Path or description of where this recording came from.
    """

    samples: np.ndarray
    sample_rate: int
    center_freq: int
    source: str

    @property
    def duration(self) -> float:
        """Duration of the recording in seconds."""
        return len(self.samples) / self.sample_rate

    @property
    def num_samples(self) -> int:
        """Total number of IQ samples."""
        return len(self.samples)


def load_raw_iq(
    path: str | Path,
    sample_rate: int,
    center_freq: int,
    dtype: str = "float32",
) -> IQRecording:
    """Load IQ samples from a raw binary file.

    Raw IQ files store interleaved I and Q values as floats:
    [IQ, Q0, I1, Q1, I2, Q2, ...]

    Each pair (I, Q) represents one complex sample.

    Args:
        path: Path to the raw IQ file.
        sample_rate: Sample rate in Hz.
        center_freq: Center frequency in Hz.
        dtype: Data type of the raw values. Common formats:
            - 'float32': 32-bit float (RTL-SDR default via GNU Radio)
            - 'uint8': 8-bit unsigned int (RTL-SDR raw output)

    Returns:
        IQRecording with complex-valued samples.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains no valid samples.
    """
    path = Path(path)

    if not path.exists():
        msg = f"IQ file not found: {path}"
        raise FileNotFoundError(msg)

    raw = np.fromfile(path, dtype=np.dtype(dtype))

    if len(raw) < 2:
        msg = f"File contains no valid IQ samples: {path}"
        raise ValueError(msg)

    if len(raw) % 2 != 0:
        raw = raw[:-1]

    # Combine interleaved I and Q into complex samples
    # raw[0::2] takes every even index (I values)
    # raw[1::2] takes every odd index (Q values)
    samples = raw[0::2] + 1j * raw[1::2]

    return IQRecording(
        samples=samples,
        sample_rate=sample_rate,
        center_freq=center_freq,
        source=str(path),
    )
