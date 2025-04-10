import sys
import time
import ftd2xx

# Denkovi constants
DENKOVI_SERIAL_PREFIX = b"DAE"  # Serial number prefix for Denkovi boards


def find_denkovi_board():
    device_count = ftd2xx.createDeviceInfoList()
    for i in range(device_count):
        info = ftd2xx.getDeviceInfoDetail(i)
        if info["serial"] and info["serial"].startswith(DENKOVI_SERIAL_PREFIX):
            return i
    return None


def set_relay_pattern(pattern):
    # Validate pattern
    if len(pattern) != 8 or not all(bit in "01" for bit in pattern):
        print("ERROR: Pattern must be 8 bits (zeros and ones)")
        return False

    # Convert to byte value
    value = int(pattern, 2)

    # Find the Denkovi board
    board_index = find_denkovi_board()
    if board_index is None:
        return False

    # Open and set the pattern
    handle = ftd2xx.open(board_index)
    handle.setBitMode(0xFF, 0x01)  # Bitbang mode
    time.sleep(0.05)

    # Send the pattern
    handle.write(bytes([value]))
    handle.close()
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python denkovi_8_relay.py <pattern>")
        return 0

    return 0 if set_relay_pattern(sys.argv[1]) else 1


if __name__ == "__main__":
    sys.exit(main())
