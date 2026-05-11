"""Tests for the IQ loader module."""

import numpy as np
import pytest

from skyguard.io.iq_loader import IQRecording, load_raw_iq


@pytest.fixture
def sample_iq_file(tmp_path):
    """Create a temporary raw IQ file with known data."""
    # Generate 100 interleaved I/Q pairs as float32
    num_samples = 100
    i_values = np.cos(np.linspace(0, 2 * np.pi, num_samples)).astype(np.float32)
    q_values = np.sin(np.linspace(0, 2 * np.pi, num_samples)).astype(np.float32)

    # Interleave: [I0, Q0, I1, Q1, ...]
    interleaved = np.empty(num_samples * 2, dtype=np.float32)
    interleaved[0::2] = i_values
    interleaved[1::2] = q_values

    file_path = tmp_path / "test.raw"
    interleaved.tofile(str(file_path))
    return file_path, num_samples


class TestIQRecording:
    def test_duration(self):
        samples = np.zeros(1000, dtype=complex)
        recording = IQRecording(
            samples=samples,
            sample_rate=1000,
            center_freq=2_400_000_000,
            source="test",
        )
        assert recording.duration == 1.0

    def test_num_samples(self):
        samples = np.zeros(500, dtype=complex)
        recording = IQRecording(
            samples=samples,
            sample_rate=1000,
            center_freq=2_400_000_000,
            source="test",
        )
        assert recording.num_samples == 500


class TestLoadRawIQ:
    def test_load_valid_file(self, sample_iq_file):
        path, num_samples = sample_iq_file
        recording = load_raw_iq(
            path,
            sample_rate=2_400_000,
            center_freq=2_400_000_000,
        )
        assert recording.num_samples == num_samples
        assert recording.sample_rate == 2_400_000
        assert recording.center_freq == 2_400_000_000
        assert np.iscomplexobj(recording.samples)

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_raw_iq(
                "nonexistent.raw",
                sample_rate=2_400_000,
                center_freq=2_400_000_000,
            )

    def test_empty_file(self, tmp_path):
        empty_file = tmp_path / "empty.raw"
        np.array([], dtype=np.float32).tofile(str(empty_file))
        with pytest.raises(ValueError, match="no valid IQ samples"):
            load_raw_iq(
                empty_file,
                sample_rate=2_400_000,
                center_freq=2_400_000_000,
            )

    def test_duration_calculation(self, sample_iq_file):
        path, num_samples = sample_iq_file
        recording = load_raw_iq(
            path,
            sample_rate=100,
            center_freq=2_400_000_000,
        )
        assert recording.duration == num_samples / 100
