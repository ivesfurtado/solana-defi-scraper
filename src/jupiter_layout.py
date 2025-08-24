from construct import Padding, Struct, Int64sl, Int16ul, Int8ul, Int64ul, Bytes
from dataclasses import dataclass
from solders.pubkey import Pubkey  # type: ignore
import base64

# Layout for Jupiter create pool events
JUPITER_CREATE_POOL_EVENT_LAYOUT = Struct(
    Padding(8),
    "timestamp" / Int64sl,               # i64
    "index" / Int16ul,                   # u16
    "creator" / Bytes(32),               # pubkey
    "base_mint" / Bytes(32),             # pubkey
    "quote_mint" / Bytes(32),            # pubkey
    "base_mint_decimals" / Int8ul,       # u8
    "quote_mint_decimals" / Int8ul,      # u8
    "base_amount_in" / Int64ul,          # u64
    "quote_amount_in" / Int64ul,         # u64
    "pool_base_amount" / Int64ul,        # u64
    "pool_quote_amount" / Int64ul,       # u64
    "minimum_liquidity" / Int64ul,       # u64
    "initial_liquidity" / Int64ul,       # u64
    "lp_token_amount_out" / Int64ul,     # u64
    "pool_bump" / Int8ul,                # u8
    "pool" / Bytes(32),                  # pubkey
    "lp_mint" / Bytes(32),               # pubkey
    "user_base_token_account" / Bytes(32),  # pubkey
    "user_quote_token_account" / Bytes(32)  # pubkey
)

# Layout for Jupiter swap events
JUPITER_SWAP_EVENT_LAYOUT = Struct(
    Padding(8),
    "timestamp" / Int64sl,               # i64
    "index" / Int16ul,                   # u16
    "creator" / Bytes(32),               # pubkey
    "base_mint" / Bytes(32),             # pubkey
    "quote_mint" / Bytes(32),            # pubkey
    "base_mint_decimals" / Int8ul,       # u8
    "quote_mint_decimals" / Int8ul,      # u8
    "base_amount_in" / Int64ul,          # u64
    "quote_amount_in" / Int64ul,         # u64
    "pool_base_amount" / Int64ul,        # u64
    "pool_quote_amount" / Int64ul,       # u64
    "minimum_liquidity" / Int64ul,       # u64
    "initial_liquidity" / Int64ul,       # u64
    "lp_token_amount_out" / Int64ul,     # u64
    "pool_bump" / Int8ul,                # u8
    "pool" / Bytes(32),                  # pubkey
    "lp_mint" / Bytes(32),               # pubkey
    "user_base_token_account" / Bytes(32),  # pubkey
    "user_quote_token_account" / Bytes(32)  # pubkey
)

@dataclass
class JupiterCreatePoolEvent:
    timestamp: int
    index: int
    creator: str
    base_mint: str
    quote_mint: str
    base_mint_decimals: int
    quote_mint_decimals: int
    base_amount_in: int
    quote_amount_in: int
    pool_base_amount: int
    pool_quote_amount: int
    minimum_liquidity: int
    initial_liquidity: int
    lp_token_amount_out: int
    pool_bump: int
    pool: str
    lp_mint: str
    user_base_token_account: str
    user_quote_token_account: str

@dataclass
class JupiterSwapEvent:
    timestamp: int
    index: int
    creator: str
    base_mint: str
    quote_mint: str
    base_mint_decimals: int
    quote_mint_decimals: int
    base_amount_in: int
    quote_amount_in: int
    pool_base_amount: int
    pool_quote_amount: int
    minimum_liquidity: int
    initial_liquidity: int
    lp_token_amount_out: int
    pool_bump: int
    pool: str
    lp_mint: str
    user_base_token_account: str
    user_quote_token_account: str

def decode_jupiter_create_pool_event(program_data_base64: str) -> JupiterCreatePoolEvent | None:
    """Decode a Jupiter create pool event from base64 encoded data."""
    try:
        raw = base64.b64decode(program_data_base64)
        p = JUPITER_CREATE_POOL_EVENT_LAYOUT.parse(raw)

        return JupiterCreatePoolEvent(
            timestamp=p.timestamp,
            index=p.index,
            creator=str(Pubkey.from_bytes(p.creator)),
            base_mint=str(Pubkey.from_bytes(p.base_mint)),
            quote_mint=str(Pubkey.from_bytes(p.quote_mint)),
            base_mint_decimals=p.base_mint_decimals,
            quote_mint_decimals=p.quote_mint_decimals,
            base_amount_in=p.base_amount_in,
            quote_amount_in=p.quote_amount_in,
            pool_base_amount=p.pool_base_amount,
            pool_quote_amount=p.pool_quote_amount,
            minimum_liquidity=p.minimum_liquidity,
            initial_liquidity=p.initial_liquidity,
            lp_token_amount_out=p.lp_token_amount_out,
            pool_bump=p.pool_bump,
            pool=str(Pubkey.from_bytes(p.pool)),
            lp_mint=str(Pubkey.from_bytes(p.lp_mint)),
            user_base_token_account=str(Pubkey.from_bytes(p.user_base_token_account)),
            user_quote_token_account=str(Pubkey.from_bytes(p.user_quote_token_account)),
        )
    except Exception:
        return None

def decode_jupiter_swap_event(program_data_base64: str) -> JupiterSwapEvent | None:
    """Decode a Jupiter swap event from base64 encoded data."""
    try:
        raw = base64.b64decode(program_data_base64)
        p = JUPITER_SWAP_EVENT_LAYOUT.parse(raw)

        return JupiterSwapEvent(
            timestamp=p.timestamp,
            index=p.index,
            creator=str(Pubkey.from_bytes(p.creator)),
            base_mint=str(Pubkey.from_bytes(p.base_mint)),
            quote_mint=str(Pubkey.from_bytes(p.quote_mint)),
            base_mint_decimals=p.base_mint_decimals,
            quote_mint_decimals=p.quote_mint_decimals,
            base_amount_in=p.base_amount_in,
            quote_amount_in=p.quote_amount_in,
            pool_base_amount=p.pool_base_amount,
            pool_quote_amount=p.pool_quote_amount,
            minimum_liquidity=p.minimum_liquidity,
            initial_liquidity=p.initial_liquidity,
            lp_token_amount_out=p.lp_token_amount_out,
            pool_bump=p.pool_bump,
            pool=str(Pubkey.from_bytes(p.pool)),
            lp_mint=str(Pubkey.from_bytes(p.lp_mint)),
            user_base_token_account=str(Pubkey.from_bytes(p.user_base_token_account)),
            user_quote_token_account=str(Pubkey.from_bytes(p.user_quote_token_account)),
        )
    except Exception:
        return None
