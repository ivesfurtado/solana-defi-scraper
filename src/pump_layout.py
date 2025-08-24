from construct import Struct, Int64ul, Bytes, Flag, PaddedString, Int8ul
from dataclasses import dataclass
from solders.pubkey import Pubkey  # type: ignore

# Layout for the 'Create' event
PUMP_CREATE_EVENT_LAYOUT = Struct(
    "name" / PaddedString(32, "utf-8"),
    "symbol" / PaddedString(10, "utf-8"),
    "uri" / PaddedString(100, "utf-8"),
    "mint" / Bytes(32),
    "bonding_curve" / Bytes(32),
    "user" / Bytes(32),
)

# Layout for the 'Trade' event
PUMP_TRADE_EVENT_LAYOUT = Struct(
    "mint" / Bytes(32),
    "sol_amount" / Int64ul,
    "token_amount" / Int64ul,
    "is_buy" / Flag,
    "user" / Bytes(32),
    "timestamp" / Int64ul,
    "virtual_sol_reserves" / Int64ul,
    "virtual_token_reserves" / Int64ul,
)

# Layout for the 'Complete' event
PUMP_COMPLETE_EVENT_LAYOUT = Struct(
    "user" / Bytes(32),
    "mint" / Bytes(32),
    "bonding_curve" / Bytes(32),
    "timestamp" / Int64ul,
)

@dataclass
class PumpCreateEvent:
    name: str
    symbol: str
    uri: str
    mint: str
    bonding_curve: str
    user: str

@dataclass
class PumpTradeEvent:
    mint: str
    sol_amount: int
    token_amount: int
    is_buy: bool
    user: str
    timestamp: int
    virtual_sol_reserves: int
    virtual_token_reserves: int

@dataclass
class PumpCompleteEvent:
    user: str
    mint: str
    bonding_curve: str
    timestamp: int

def decode_pump_create_event(program_data_bytes: bytes) -> PumpCreateEvent | None:
    """Decode a pump.fun create event from raw bytes."""
    try:
        p = PUMP_CREATE_EVENT_LAYOUT.parse(program_data_bytes)
        return PumpCreateEvent(
            name=p.name.rstrip('\x00'),
            symbol=p.symbol.rstrip('\x00'),
            uri=p.uri.rstrip('\x00'),
            mint=str(Pubkey.from_bytes(p.mint)),
            bonding_curve=str(Pubkey.from_bytes(p.bonding_curve)),
            user=str(Pubkey.from_bytes(p.user)),
        )
    except Exception:
        return None

def decode_pump_trade_event(program_data_bytes: bytes) -> PumpTradeEvent | None:
    """Decode a pump.fun trade event from raw bytes."""
    try:
        p = PUMP_TRADE_EVENT_LAYOUT.parse(program_data_bytes)
        return PumpTradeEvent(
            mint=str(Pubkey.from_bytes(p.mint)),
            sol_amount=p.sol_amount,
            token_amount=p.token_amount,
            is_buy=p.is_buy,
            user=str(Pubkey.from_bytes(p.user)),
            timestamp=p.timestamp,
            virtual_sol_reserves=p.virtual_sol_reserves,
            virtual_token_reserves=p.virtual_token_reserves,
        )
    except Exception:
        return None

def decode_pump_complete_event(program_data_bytes: bytes) -> PumpCompleteEvent | None:
    """Decode a pump.fun complete event from raw bytes."""
    try:
        p = PUMP_COMPLETE_EVENT_LAYOUT.parse(program_data_bytes)
        return PumpCompleteEvent(
            user=str(Pubkey.from_bytes(p.user)),
            mint=str(Pubkey.from_bytes(p.mint)),
            bonding_curve=str(Pubkey.from_bytes(p.bonding_curve)),
            timestamp=p.timestamp,
        )
    except Exception:
        return None
