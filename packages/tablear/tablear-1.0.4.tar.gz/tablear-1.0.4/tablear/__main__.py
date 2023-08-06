import argparse
from .UserSetup import main as setup_main
from .ARTable import main as demo_main
import os

uidir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui')

def main():
    parser = argparse.ArgumentParser(description="Runs the AR table setup or a demo")
    parser.add_argument("mode",choices=["setup", "demo"],help="Run setup, or demo?")
    args = parser.parse_args()
    if args.mode == 'setup':
        # Run setup with a default 
        setup_main(os.path.join(uidir, 'base'))
    elif args.mode == 'demo':
        demo_main()

if __name__ == '__main__':
    main()