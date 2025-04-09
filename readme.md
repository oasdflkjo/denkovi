# Denkovi Relay Protocol — Reverse Engineered

A minimal Python library for controlling Denkovi USB relay boards via raw binary protocol.  
Designed for simplicity, clarity, and direct control. Written by Claude 3.7.

---

## Overview

This project documents a reverse-engineered protocol used to control Denkovi relay boards over serial.  
The communication is straightforward: each bit in the data byte corresponds to a relay's state.

- **1** = Relay ON  
- **0** = Relay OFF  

---

## Protocol

```python
0b00000001  # Relay 0 ON
0b00000101  # Relays 0 and 2 ON
```

---

## Installation

Clone this repository or copy `denkovi_relay.py` into your project directory.  

Compatibility with different python/pyserial version is not tested.
```
Versions used while developping:
Python    3.12.9
pyserial  3.5
```


---

## Usage (Python)

```python
from denkovi_relay import DenkoviRelay

relay = DenkoviRelay('COM8')

try:
    relay.connect()

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

# Turn on all relays
python denkovi_relay.py COM8 11111111

# Error message if incorrect arguments:
# Usage: python denkovi_relay.py <port> <pattern>
# Example (8 relays): python denkovi_relay.py COM8 10101010
# Example (16 relays): python denkovi_relay.py COM8 1010101010101010
```

---

## Contributing

If you discover improvements or board variants, PRs are welcome.

---

## License

This project is licensed under the MIT License.
