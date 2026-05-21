#!/usr/bin/env python3
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Countdown CLI tool that counts down (or up) to Liftoff!"
    )
    parser.add_argument(
        "number",
        nargs="?",
        help="The positive integer to start counting from (or end at if --reverse is set)"
    )
    parser.add_argument(
        "-r", "--reverse",
        action="store_true",
        help="Count up from 1 to the number instead of counting down"
    )

    args = parser.parse_args()

    # Manual validation for missing argument
    if args.number is None:
        print("Error: Missing required argument 'number'.", file=sys.stderr)
        parser.print_usage(sys.stderr)
        sys.exit(1)

    # Manual validation for integer check
    try:
        count_limit = int(args.number)
    except ValueError:
        print(f"Error: '{args.number}' is not a valid integer.", file=sys.stderr)
        sys.exit(1)

    # Manual validation for positive integer check
    if count_limit < 1:
        print(f"Error: {count_limit} is not positive. The count must be 1 or greater.", file=sys.stderr)
        sys.exit(1)

    # Perform the counting
    if args.reverse:
        for i in range(1, count_limit + 1):
            print(i)
    else:
        for i in range(count_limit, 0, -1):
            print(i)
            
    print("Liftoff!")

if __name__ == "__main__":
    main()
