import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.wss import start_websocket


def main():
    """Main entry point for the Solana DeFi Scraper."""
    print("Starting Solana DeFi Scraper...")
    print("Monitoring Jupiter, Pump.fun, and Raydium protocols...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        start_websocket()
    except KeyboardInterrupt:
        print("\nShutdown requested by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
