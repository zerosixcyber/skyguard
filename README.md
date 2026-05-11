# SkyGuard

Open-source passive drone detection system using SDR and RF signal analysis.

## Overview

SkyGuard detects drones in the surrounding airspace by passively analyzing
radio frequency signals. It identifies known drone communication protocols
(WiFi, DJI OcuSync, FPV frequencies) using Software Defined Radio without
emitting any signals.

## Status

**Early Development** — This project is in the initial development phase.

## Features (Planned)

- Passive RF signal capture via RTL-SDR
- Drone protocol identification (DJI, FPV, WiFi-based)
- Real-time signal analysis and classification
- Alert system for detected drones
- Support for pre-recorded IQ sample analysis

## Requirements

- Python 3.12+
- RTL-SDR compatible device (for live capture, optional)

## Setup

```bash
git clone git@github.com:zerosixcyber/skyguard.git
cd skyguard
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -e ".[dev]"
pre-commit install
```

## Usage

```bash
make lint      # Run linter
make format    # Format code
make test      # Run tests
make test-cov  # Run tests with coverage
```

## License

MIT
