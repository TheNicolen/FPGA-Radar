"""Analytical monostatic radar budget. No detection or FMCW simulation."""
import argparse
import hashlib
import json
import math
from pathlib import Path

C = 299_792_458.0
K_B = 1.380649e-23


def calculate(config):
    """Return theoretical powers in dBm and SNR in dB; SI input names."""
    positive = ('frequency_hz', 'range_m', 'rcs_m2',
                'noise_bandwidth_hz', 'temperature_k')
    other = ('tx_power_dbm', 'tx_gain_dbi', 'rx_gain_dbi',
             'loss_db', 'noise_figure_db', 'target_snr_db')
    for key in positive + other:
        value = config[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f'{key} must be numeric')
        if not math.isfinite(value):
            raise ValueError(f'{key} must be finite')
    for key in positive:
        if config[key] <= 0:
            raise ValueError(f'{key} must be positive')
    if config['loss_db'] < 0 or config['noise_figure_db'] < 0:
        raise ValueError('loss_db and noise_figure_db must be nonnegative')
    wavelength = C / config['frequency_hz']
    received = (config['tx_power_dbm'] + config['tx_gain_dbi']
                + config['rx_gain_dbi'] + 20 * math.log10(wavelength)
                + 10 * math.log10(config['rcs_m2'])
                - 30 * math.log10(4 * math.pi)
                - 40 * math.log10(config['range_m']) - config['loss_db'])
    noise = (10 * math.log10(K_B * config['temperature_k']
                            * config['noise_bandwidth_hz']) + 30
             + config['noise_figure_db'])
    snr = received - noise
    return {
        'evidence': 'TEORICO',
        'model': 'monostatic_equivalent_free_space',
        'wavelength_m': wavelength,
        'received_power_dbm': received,
        'noise_power_dbm': noise,
        'snr_before_processing_db': snr,
        'ideal_processing_gain_required_db': max(0, config['target_snr_db'] - snr),
        'limitations': 'No clutter, leakage, phase noise or detection statistics; '
                       'noise bandwidth is not automatically FMCW sweep bandwidth.'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    args = parser.parse_args()
    raw = args.config.read_bytes()
    config = json.loads(raw)
    result = calculate(config)
    result['config_sha256'] = hashlib.sha256(raw).hexdigest()
    result['config'] = config
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
