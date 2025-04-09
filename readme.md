# Denkovi Relay Protocol — Reverse Engineered

A minimal Python library for controlling Denkovi USB relay boards via raw binary protocol.  
Designed for simplicity, clarity, and direct control.

---

## Overview

This project documents a reverse-engineered protocol used to control Denkovi relay boards over serial.  
The communication is straightforward: each bit in the data byte corresponds to a relay's state.

- **1** = Relay ON  
- **0** = Relay OFF  
- Each byte controls up to 8 relays  

---

## Protocol

```python
# 8-relay board: one byte
0b00000001  # Relay 0 ON
0b00000101  # Relays 0 and 2 ON
```

---

## Installation

Clone this repository or copy `denkovi_relay.py` into your project directory.  
Python 3.6+ and `pyserial` are required.

```bash
pip install pyserial
```

---

## Usage (Python)

```python
from denkovi_relay import DenkoviRelay

relay = DenkoviRelay('COM8')

try:
    relay.connect()

    # Turn on all relays
    relay.set_pattern(0xFF)

    # Turn on every other relay
    relay.set_pattern(0xAA)

    # Set relays using a binary string
    relay.set_pattern('10101010')
finally:
    relay.disconnect()
```

Note: Attempting to set a pattern without connecting will raise a RuntimeError.

---

## Usage (Command Line)

```bash
# Syntax: python denkovi_relay.py <port> <pattern>
# Pattern can be binary string or hex (e.g., 0xFF)

# Turn on all relays
python denkovi_relay.py COM8 11111111

# Alternate pattern
python denkovi_relay.py COM8 0xAA

# Error message if incorrect arguments:
# Usage: python denkovi_relay.py <port> <pattern>
# Example (8 relays): python denkovi_relay.py COM8 10101010
# Example (16 relays): python denkovi_relay.py COM8 1010101010101010
```

---

## Contributing

If you discover improvements or board variants, contributions are welcome.  
Please submit a pull request or open an issue.

---

## License

This project is licensed under the MIT License.
