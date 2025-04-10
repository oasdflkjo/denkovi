# Denkovi Relay Controller

_by Claude 3.7_

A Python library for controlling Denkovi USB relay boards using two different approaches:
1. **Direct FTDI control** (8-relay boards) - Bypasses serial communication because init signal can't be sent trough com port :D
2. **Serial protocol** (16-relay boards) - Uses the official protocol as per the Denkovi manual


## Overview

This project offers two implementations for controlling Denkovi relay boards:

### 1. Direct FTDI Control (8-relay boards)
- Bypasses serial communications entirely
- Works directly with the FTDI chip using the ftd2xx library


### 2. Serial Protocol (16-relay boards)
- Uses standard serial port communication
- Follows the official Denkovi protocol
- Supports 16-relay models

Both approaches use the same fundamental principle: each bit in a byte controls one relay:
- **1** = Relay ON  
- **0** = Relay OFF  

## Requirements

### For 8-relay boards (FTDI approach):
- Python 3.x
- ftd2xx library (`pip install ftd2xx`)
- FTDI drivers installed on your system ([Download from FTDI](https://ftdichip.com/drivers/))

### For 16-relay boards (Serial approach):
- Python 3.x
- pyserial library (`pip install pyserial`)

## Usage: 8-Relay Board (FTDI Approach)

### Python
```python
import denkovi_8_relay

# Set relay pattern (8 bits)
denkovi_8_relay.set_relay_pattern('10101010')
```

### Command Line
```bash
# Set a pattern - all ones and zeros, must be 8 bits
python denkovi_8_relay.py 10101010

# Turn on all relays
python denkovi_8_relay.py 11111111
```



## Usage: 16-Relay Board (Serial Approach)

### Python
```python
from denkovi_16_relay import DenkoviRelay

relay = DenkoviRelay('COM8')

try:
    relay.connect()
    
    # Set relays using a binary string
    relay.set_pattern('1010101010101010')
    
finally:
    relay.disconnect()
```

### Command Line
```bash
# Syntax: python denkovi_16_relay.py <port> <pattern>

# Turn on all relays
python denkovi_16_relay.py COM8 1111111111111111

# Turn on specific relays (16-bit pattern)
python denkovi_16_relay.py COM8 1010101010101010
```




## Why Two Different Approaches?

### 8-Relay Direct FTDI Control

Traditional serial port methods often fail with Denkovi boards because:
1. The board can become unresponsive due to FTDI chip sleep mode
2. Serial communication requires precise timing and wake-up sequences
3. Windows COM port handling introduces additional complexity

Using direct FTDI control bypasses these issues by:
1. Directly accessing the FTDI chip through its driver
2. Working at the USB level rather than through serial abstractions
3. Providing more reliable control of the hardware

### 16-Relay Serial Protocol

The 16-relay boards require a more complex protocol that sends two bytes 
for controlling all 16 relays. This implementation follows the official 
Denkovi documentation and works well for the 16-relay models.

## Contributing

If you discover improvements or board variants, PRs are welcome.



## License

This project is licensed under the MIT License.
