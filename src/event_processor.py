import base64
from typing import Union, Optional
from dataclasses import asdict

from .jupiter_layout import (
    decode_jupiter_create_pool_event,
    decode_jupiter_swap_event,
    JupiterCreatePoolEvent,
    JupiterSwapEvent
)
from .pump_layout import (
    decode_pump_create_event,
    decode_pump_trade_event,
    decode_pump_complete_event,
    PumpCreateEvent,
    PumpTradeEvent,
    PumpCompleteEvent
)
from .raydium_layout import (
    decode_raydium_init_pool_event,
    decode_raydium_swap_event,
    decode_raydium_liquidity_event,
    decode_raydium_event,
    RaydiumInitPoolEvent,
    RaydiumSwapEvent,
    RaydiumLiquidityEvent
)
from .constants import JUPITER_PROGRAM_ID, PUMP_FUN_PROGRAM_ID, RAYDIUM_V4_PROGRAM_ID

SolanaEvent = Union[
    JupiterCreatePoolEvent,
    JupiterSwapEvent,
    PumpCreateEvent,
    PumpTradeEvent,
    PumpCompleteEvent,
    RaydiumInitPoolEvent,
    RaydiumSwapEvent,
    RaydiumLiquidityEvent
]

class EventProcessor:
    """Processes Solana transaction logs and extracts DEX events."""
    
    def __init__(self):
        self.event_handlers = {
            "jupiter_swap": self._handle_jupiter_swap,
            "jupiter_create_pool": self._handle_jupiter_create_pool,
            "pump_create": self._handle_pump_create,
            "pump_trade": self._handle_pump_trade,
            "pump_complete": self._handle_pump_complete,
            "raydium_init_pool": self._handle_raydium_init_pool,
            "raydium_swap": self._handle_raydium_swap,
            "raydium_liquidity": self._handle_raydium_liquidity,
        }
        
    def process_logs(self, logs: list[str]) -> Optional[SolanaEvent]:
        """Process transaction logs and return any decoded events."""
        logs_str = "".join(logs)
        
        if "JUP" in logs_str or JUPITER_PROGRAM_ID in logs_str:
            return self._process_jupiter_logs(logs, logs_str)
        
        elif RAYDIUM_V4_PROGRAM_ID in logs_str or "ray_log:" in logs_str:
            return self._process_raydium_logs(logs, logs_str)
        
        elif PUMP_FUN_PROGRAM_ID in logs_str:
            return self._process_pump_logs(logs, logs_str)
        
        return self._process_generic_logs(logs, logs_str)
    
    def _process_jupiter_logs(self, logs: list[str], logs_str: str) -> Optional[SolanaEvent]:
        """Process Jupiter-specific logs."""
        if "Program log: Instruction: Swap" in logs_str:
            return self._extract_and_decode(logs, decode_jupiter_swap_event)
        
        return self._extract_and_decode(logs, decode_jupiter_create_pool_event)
    
    def _process_raydium_logs(self, logs: list[str], logs_str: str) -> Optional[SolanaEvent]:
        """Process Raydium-specific logs."""
        for decoder in [
            decode_raydium_swap_event,
            decode_raydium_liquidity_event,
            decode_raydium_init_pool_event
        ]:
            event = self._extract_and_decode(logs, decoder)
            if event:
                return event
        
        return self._extract_and_decode_bytes(logs, decode_raydium_event)
    
    def _process_pump_logs(self, logs: list[str], logs_str: str) -> Optional[SolanaEvent]:
        """Process pump.fun-specific logs."""
        for decoder in [
            lambda b64: decode_pump_create_event(base64.b64decode(b64)),
            lambda b64: decode_pump_trade_event(base64.b64decode(b64)),
            lambda b64: decode_pump_complete_event(base64.b64decode(b64))
        ]:
            event = self._extract_and_decode(logs, decoder)
            if event:
                return event
        
        return None
    
    def _process_generic_logs(self, logs: list[str], logs_str: str) -> Optional[SolanaEvent]:
        """Fallback processing for any logs with program data."""
        if "Program data: " not in logs_str:
            return None
        
        for decoder in [
            decode_jupiter_swap_event,
            decode_jupiter_create_pool_event,
            lambda b64: decode_pump_create_event(base64.b64decode(b64)),
            lambda b64: decode_pump_trade_event(base64.b64decode(b64)),
            lambda b64: decode_pump_complete_event(base64.b64decode(b64)),
            decode_raydium_swap_event,
            decode_raydium_liquidity_event,
            decode_raydium_init_pool_event,
        ]:
            event = self._extract_and_decode(logs, decoder)
            if event:
                return event
        
        return None
    
    def _extract_and_decode(self, logs: list[str], decoder_func) -> Optional[SolanaEvent]:
        """Extract program data from logs and decode using the provided function."""
        for log_entry in logs:
            if log_entry.startswith("Program data: "):
                b64 = log_entry.split("Program data: ", 1)[1]
                try:
                    event = decoder_func(b64)
                    if event:
                        return event
                except Exception:
                    continue
        return None
    
    def _extract_and_decode_bytes(self, logs: list[str], decoder_func) -> Optional[SolanaEvent]:
        """Extract program data from logs and decode using a bytes-based decoder."""
        for log_entry in logs:
            if log_entry.startswith("Program data: "):
                b64 = log_entry.split("Program data: ", 1)[1]
                try:
                    raw_bytes = base64.b64decode(b64)
                    event = decoder_func(raw_bytes)
                    if event:
                        return event
                except Exception:
                    continue
        return None
    
    def _handle_jupiter_swap(self, event: JupiterSwapEvent):
        """Handle Jupiter swap event."""
        print("=== JUPITER SWAP EVENT ===")
        print(asdict(event), flush=True)
    
    def _handle_jupiter_create_pool(self, event: JupiterCreatePoolEvent):
        """Handle Jupiter create pool event."""
        print("=== JUPITER CREATE POOL EVENT ===")
        print(asdict(event))
    
    def _handle_pump_create(self, event: PumpCreateEvent):
        """Handle pump.fun create event."""
        print("=== PUMP CREATE EVENT ===")
        print(asdict(event))
    
    def _handle_pump_trade(self, event: PumpTradeEvent):
        """Handle pump.fun trade event."""
        print("=== PUMP TRADE EVENT ===")
        print(asdict(event))
    
    def _handle_pump_complete(self, event: PumpCompleteEvent):
        """Handle pump.fun complete event."""
        print("=== PUMP COMPLETE EVENT ===")
        print(asdict(event))
    
    def _handle_raydium_init_pool(self, event: RaydiumInitPoolEvent):
        """Handle Raydium init pool event."""
        print("=== RAYDIUM INIT POOL EVENT ===")
        print(asdict(event))
    
    def _handle_raydium_swap(self, event: RaydiumSwapEvent):
        """Handle Raydium swap event."""
        print("=== RAYDIUM SWAP EVENT ===")
        print(asdict(event))
    
    def _handle_raydium_liquidity(self, event: RaydiumLiquidityEvent):
        """Handle Raydium liquidity event."""
        print("=== RAYDIUM LIQUIDITY EVENT ===")
        print(asdict(event))
    
    def handle_event(self, event: SolanaEvent):
        """Handle any decoded event by dispatching to the appropriate handler."""
        event_type = type(event).__name__
        
        if isinstance(event, JupiterSwapEvent):
            self._handle_jupiter_swap(event)
        elif isinstance(event, JupiterCreatePoolEvent):
            self._handle_jupiter_create_pool(event)
        elif isinstance(event, PumpCreateEvent):
            self._handle_pump_create(event)
        elif isinstance(event, PumpTradeEvent):
            self._handle_pump_trade(event)
        elif isinstance(event, PumpCompleteEvent):
            self._handle_pump_complete(event)
        elif isinstance(event, RaydiumInitPoolEvent):
            self._handle_raydium_init_pool(event)
        elif isinstance(event, RaydiumSwapEvent):
            self._handle_raydium_swap(event)
        elif isinstance(event, RaydiumLiquidityEvent):
            self._handle_raydium_liquidity(event)
        else:
            print(f"=== UNKNOWN EVENT TYPE: {event_type} ===")
            print(asdict(event))
