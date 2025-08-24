# Solana DeFi Scraper

A real-time Solana blockchain transaction scraper that monitors and extracts DeFi events from major decentralized exchanges and protocols on the Solana network.

## Overview

This project provides a comprehensive WebSocket-based solution for monitoring and parsing DeFi activity across three major Solana protocols:

- **Jupiter Aggregator**: DEX aggregation protocol for optimal swap routing
- **Pump.fun**: Meme token creation and trading platform
- **Raydium V4**: Leading AMM (Automated Market Maker) on Solana

The scraper connects to Solana's mainnet WebSocket API to monitor program logs in real-time, automatically parsing and extracting structured event data from raw transaction logs.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Solana RPC    │───▶│  WebSocket      │───▶│  Event          │
│   WebSocket     │    │  Connection     │    │  Processor      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Jupiter       │    │   Pump.fun      │    │   Raydium       │
│   Layout        │    │   Layout        │    │   Layout        │
│   Decoder       │    │   Decoder       │    │   Decoder       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Supported Events

#### Jupiter Aggregator
- **Pool Creation**: New liquidity pool events with detailed token information
- **Swap Events**: Token swap transactions with routing information
- Captures: timestamps, token pairs, amounts, pool details, user accounts

#### Pump.fun
- **Token Creation**: New meme token launches
- **Trade Events**: Buy/sell transactions with pricing data
- **Pool Completion**: Graduation events to other DEXs
- Captures: token metadata, trading volumes, price impact, virtual reserves

#### Raydium V4 AMM
- **Pool Initialization**: New AMM pool creation events
- **Swap Transactions**: Direct AMM swap events
- **Liquidity Events**: Add/remove liquidity operations
- Captures: AMM pool data, reserve amounts, fees, market information

## Installation

### Prerequisites
- Python 3.12 or higher
- Poetry (recommended) or pip

### Using Poetry (Recommended)

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd solana-defi-scraper
   poetry install
   ```

3. **Run the scraper**:
   ```bash
   poetry run solana-defi-scraper
   ```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd solana-defi-scraper

# Install dependencies
pip install websocket-client construct solders

# Run the scraper
python main.py
```

## Usage

### Running the Scraper

The scraper provides multiple execution methods:

**Method 1: Poetry script (recommended)**
```bash
poetry run solana-defi-scraper
```

**Method 2: Direct execution**
```bash
python main.py
```

**Method 3: Development mode**
```bash
poetry shell
python main.py
```

### Example Output

```
=== JUPITER SWAP EVENT ===
{
  'timestamp': 1756058012,
  'creator': 'CUxEstt5N9XwXjb3N64VwQX5PBcJEREJGwLfPgXcLdaN',
  'base_mint': 'C6Wh3afuvkJFwtpuei43ajW46k7dtqrh86C1MNTkcYyj',
  'quote_mint': '5r3Ki3KewWN6GFainpVwYmoVzDGMBXGsUZkx7qefjH7n',
  'base_amount_in': 10246974248163467145,
  'quote_amount_in': 2161851253173627346
}

=== PUMP TRADE EVENT ===
{
  'mint': 'Dn8BWWfCn86k3CWkiGRxUcmEz4qtbTPXWyi93pPCa4Ti',
  'sol_amount': 6878069681956846973,
  'token_amount': 283400000,
  'is_buy': True,
  'user': 'B3nTJKVpGZrXLBMTbb6uES3orAyZHNFZPASWcqB49uWn'
}

=== RAYDIUM SWAP EVENT ===
{
  'amm_id': 'BTJRV25Lm36MprBCbVNyp1UKyuF7V3bZuumS5qm7iKUK',
  'user': 'FHudhLSKMydbFVYeHeCiwiTgKA2maqmJ4U7DJf9KfbrF',
  'amount_in': 8430738502437568512,
  'amount_out': 360287970189639855
}
```
### Adding New Protocols

To add support for a new Solana DeFi protocol:

1. **Add program ID** in `src/constants.py`:
   ```python
   NEW_PROTOCOL_PROGRAM_ID = "YourProgramIdHere..."
   ```

2. **Create layout definitions** in `src/new_protocol_layout.py`:
   ```python
   from construct import Struct, Int64ul, Bytes
   from dataclasses import dataclass
   
   @dataclass
   class NewProtocolEvent:
       # Define your event structure
       pass
   
   NEW_PROTOCOL_LAYOUT = Struct(
       # Define binary layout
   )
   ```

3. **Add decoder functions** with proper error handling
4. **Integrate event handlers** in `src/event_processor.py`
5. **Subscribe to program logs** in `src/wss.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
