"""RadarLink UDP detection decoder, for legacy RADR and azimuth RAD2."""
import struct

PACKET = struct.Struct('!4sIIHIhHBB')
PACKET_AZ = struct.Struct('!4sIIHIhHBBh')
PORT = 5005

def decode_packet(data):
    if len(data) == PACKET.size and data[:4] == b'RADR':
        fields = PACKET.unpack(data)
        azimuth = None
    elif len(data) == PACKET_AZ.size and data[:4] == b'RAD2':
        fields = PACKET_AZ.unpack(data)
        angle = fields[-1]
        if not -18000 <= angle < 18000:
            raise ValueError('azimut fuera de rango')
        azimuth = angle / 100.0
        fields = fields[:-1]
    else:
        raise ValueError('firma o longitud RADR/RAD2 incorrecta')
    _, seq, ticks, target_id, distance_cm, velocity, snr, state, reserved = fields
    return {
        'seq': seq, 'ticks': ticks, 'id': target_id,
        'range_m': distance_cm / 100.0, 'velocity_mps': velocity / 100.0,
        'snr_db': snr / 10.0, 'state': state, 'reserved': reserved,
        'azimuth_deg': azimuth
    }
