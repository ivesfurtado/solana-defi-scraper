from construct import Struct, Int64ul, Int8ul, Bytes, Flag, Padding, Int64sl
from dataclasses import dataclass
from solders.pubkey import Pubkey  # type: ignore
import base64

# Layout for pool initialization event
RAYDIUM_INIT_POOL_EVENT_LAYOUT = Struct(
    Padding(8),  # Event discriminator
    "nonce" / Int64ul,
    "open_time" / Int64ul,
    "init_pc_amount" / Int64ul,
    "init_coin_amount" / Int64ul,
    "base_mint" / Bytes(32),
    "quote_mint" / Bytes(32),
    "lp_mint" / Bytes(32),
    "amm_id" / Bytes(32),
    "amm_authority" / Bytes(32),
    "amm_open_orders" / Bytes(32),
    "amm_target_orders" / Bytes(32),
    "pool_coin_token_account" / Bytes(32),
    "pool_pc_token_account" / Bytes(32),
    "pool_withdraw_queue" / Bytes(32),
    "pool_lp_token_account" / Bytes(32),
    "serum_market" / Bytes(32),
)

# Layout for swap events
RAYDIUM_SWAP_EVENT_LAYOUT = Struct(
    Padding(8),  # Event discriminator
    "amm_id" / Bytes(32),
    "user" / Bytes(32),
    "direction" / Int8ul,  # 0 = base to quote, 1 = quote to base
    "amount_in" / Int64ul,
    "amount_out" / Int64ul,
    "fee_amount" / Int64ul,
    "base_reserve_before" / Int64ul,
    "quote_reserve_before" / Int64ul,
    "base_reserve_after" / Int64ul,
    "quote_reserve_after" / Int64ul,
    "timestamp" / Int64sl,
)

# Layout for liquidity events
RAYDIUM_LIQUIDITY_EVENT_LAYOUT = Struct(
    Padding(8),  # Event discriminator
    "amm_id" / Bytes(32),
    "user" / Bytes(32),
    "is_deposit" / Flag,  # True for deposit, False for withdraw
    "base_amount" / Int64ul,
    "quote_amount" / Int64ul,
    "lp_amount" / Int64ul,
    "base_reserve_after" / Int64ul,
    "quote_reserve_after" / Int64ul,
    "lp_supply_after" / Int64ul,
    "timestamp" / Int64sl,
)

@dataclass
class RaydiumInitPoolEvent:
    nonce: int
    open_time: int
    init_pc_amount: int
    init_coin_amount: int
    base_mint: str
    quote_mint: str
    lp_mint: str
    amm_id: str
    amm_authority: str
    amm_open_orders: str
    amm_target_orders: str
    pool_coin_token_account: str
    pool_pc_token_account: str
    pool_withdraw_queue: str
    pool_lp_token_account: str
    serum_market: str

@dataclass
class RaydiumSwapEvent:
    amm_id: str
    user: str
    direction: int  # 0 = base to quote, 1 = quote to base
    amount_in: int
    amount_out: int
    fee_amount: int
    base_reserve_before: int
    quote_reserve_before: int
    base_reserve_after: int
    quote_reserve_after: int
    timestamp: int

@dataclass
class RaydiumLiquidityEvent:
    amm_id: str
    user: str
    is_deposit: bool
    base_amount: int
    quote_amount: int
    lp_amount: int
    base_reserve_after: int
    quote_reserve_after: int
    lp_supply_after: int
    timestamp: int

def decode_raydium_init_pool_event(program_data_base64: str) -> RaydiumInitPoolEvent | None:
    """Decode a Raydium init pool event from base64 encoded data."""
    try:
        raw = base64.b64decode(program_data_base64)
        p = RAYDIUM_INIT_POOL_EVENT_LAYOUT.parse(raw)

        return RaydiumInitPoolEvent(
            nonce=p.nonce,
            open_time=p.open_time,
            init_pc_amount=p.init_pc_amount,
            init_coin_amount=p.init_coin_amount,
            base_mint=str(Pubkey.from_bytes(p.base_mint)),
            quote_mint=str(Pubkey.from_bytes(p.quote_mint)),
            lp_mint=str(Pubkey.from_bytes(p.lp_mint)),
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            amm_authority=str(Pubkey.from_bytes(p.amm_authority)),
            amm_open_orders=str(Pubkey.from_bytes(p.amm_open_orders)),
            amm_target_orders=str(Pubkey.from_bytes(p.amm_target_orders)),
            pool_coin_token_account=str(Pubkey.from_bytes(p.pool_coin_token_account)),
            pool_pc_token_account=str(Pubkey.from_bytes(p.pool_pc_token_account)),
            pool_withdraw_queue=str(Pubkey.from_bytes(p.pool_withdraw_queue)),
            pool_lp_token_account=str(Pubkey.from_bytes(p.pool_lp_token_account)),
            serum_market=str(Pubkey.from_bytes(p.serum_market)),
        )
    except Exception:
        return None

def decode_raydium_swap_event(program_data_base64: str) -> RaydiumSwapEvent | None:
    """Decode a Raydium swap event from base64 encoded data."""
    try:
        raw = base64.b64decode(program_data_base64)
        p = RAYDIUM_SWAP_EVENT_LAYOUT.parse(raw)

        return RaydiumSwapEvent(
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            user=str(Pubkey.from_bytes(p.user)),
            direction=p.direction,
            amount_in=p.amount_in,
            amount_out=p.amount_out,
            fee_amount=p.fee_amount,
            base_reserve_before=p.base_reserve_before,
            quote_reserve_before=p.quote_reserve_before,
            base_reserve_after=p.base_reserve_after,
            quote_reserve_after=p.quote_reserve_after,
            timestamp=p.timestamp,
        )
    except Exception:
        return None

def decode_raydium_liquidity_event(program_data_base64: str) -> RaydiumLiquidityEvent | None:
    """Decode a Raydium liquidity event from base64 encoded data."""
    try:
        raw = base64.b64decode(program_data_base64)
        p = RAYDIUM_LIQUIDITY_EVENT_LAYOUT.parse(raw)

        return RaydiumLiquidityEvent(
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            user=str(Pubkey.from_bytes(p.user)),
            is_deposit=p.is_deposit,
            base_amount=p.base_amount,
            quote_amount=p.quote_amount,
            lp_amount=p.lp_amount,
            base_reserve_after=p.base_reserve_after,
            quote_reserve_after=p.quote_reserve_after,
            lp_supply_after=p.lp_supply_after,
            timestamp=p.timestamp,
        )
    except Exception:
        return None

def decode_raydium_event(program_data_bytes: bytes) -> RaydiumInitPoolEvent | RaydiumSwapEvent | RaydiumLiquidityEvent | None:
    """Try to decode any Raydium event from raw bytes."""
    # Try init pool event first
    try:
        p = RAYDIUM_INIT_POOL_EVENT_LAYOUT.parse(program_data_bytes)
        return RaydiumInitPoolEvent(
            nonce=p.nonce,
            open_time=p.open_time,
            init_pc_amount=p.init_pc_amount,
            init_coin_amount=p.init_coin_amount,
            base_mint=str(Pubkey.from_bytes(p.base_mint)),
            quote_mint=str(Pubkey.from_bytes(p.quote_mint)),
            lp_mint=str(Pubkey.from_bytes(p.lp_mint)),
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            amm_authority=str(Pubkey.from_bytes(p.amm_authority)),
            amm_open_orders=str(Pubkey.from_bytes(p.amm_open_orders)),
            amm_target_orders=str(Pubkey.from_bytes(p.amm_target_orders)),
            pool_coin_token_account=str(Pubkey.from_bytes(p.pool_coin_token_account)),
            pool_pc_token_account=str(Pubkey.from_bytes(p.pool_pc_token_account)),
            pool_withdraw_queue=str(Pubkey.from_bytes(p.pool_withdraw_queue)),
            pool_lp_token_account=str(Pubkey.from_bytes(p.pool_lp_token_account)),
            serum_market=str(Pubkey.from_bytes(p.serum_market)),
        )
    except Exception:
        pass

    # Try swap event
    try:
        p = RAYDIUM_SWAP_EVENT_LAYOUT.parse(program_data_bytes)
        return RaydiumSwapEvent(
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            user=str(Pubkey.from_bytes(p.user)),
            direction=p.direction,
            amount_in=p.amount_in,
            amount_out=p.amount_out,
            fee_amount=p.fee_amount,
            base_reserve_before=p.base_reserve_before,
            quote_reserve_before=p.quote_reserve_before,
            base_reserve_after=p.base_reserve_after,
            quote_reserve_after=p.quote_reserve_after,
            timestamp=p.timestamp,
        )
    except Exception:
        pass

    # Try liquidity event
    try:
        p = RAYDIUM_LIQUIDITY_EVENT_LAYOUT.parse(program_data_bytes)
        return RaydiumLiquidityEvent(
            amm_id=str(Pubkey.from_bytes(p.amm_id)),
            user=str(Pubkey.from_bytes(p.user)),
            is_deposit=p.is_deposit,
            base_amount=p.base_amount,
            quote_amount=p.quote_amount,
            lp_amount=p.lp_amount,
            base_reserve_after=p.base_reserve_after,
            quote_reserve_after=p.quote_reserve_after,
            lp_supply_after=p.lp_supply_after,
            timestamp=p.timestamp,
        )
    except Exception:
        pass

    return None
