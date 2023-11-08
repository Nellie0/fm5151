import argparse
import sys
from bs import BSCall, BSPut
from mc import mc
from bm import bm_european, bm_american

def main():
    parser = argparse.ArgumentParser(description="Option Pricing Calculator")
    parser.add_argument("--method", choices=["black_scholes", "binomial_european", "binomial_american", "monte_carlo"],
                        help="Pricing method (Black-Scholes, Binomial European, Binomial American, Monte Carlo)")
    parser.add_argument("--type", choices = ["Call", "Put"], help = "Type of Option (Call Option or Put Option)")
    parser.add_argument("--S", type=float, help="Current stock price")
    parser.add_argument("--K", type=float, help="Strike price")
    parser.add_argument("--T", type=float, help="Time to expiration (in years)")
    parser.add_argument("--r", type=float, help="Risk-free interest rate")
    parser.add_argument("--sigma", type = float, help="Volatility")
    parser.add_argument("--q", type = float, help="Dividend yield")
    parser.add_argument("--n", type=int, help="Number of time steps (for binomial method)", nargs='?', default=None)
    parser.add_argument("--num", type=int, help="Number of simulations (for Monte Carlo method)", nargs='?', default=None)
    parser.add_argument("--basic_anti", choices = ["Basic", "Antithetic"], help="Basic Monte Carlo estimation or Antithetic Monte Carlo estimation", nargs = "?", default = None)

    # This check would indicate no arguments provided (argv[0] is always the
    # name of the script)
    if len(sys.argv) == 1:
        parser.print_usage()
        exit(0)
    
    args = parser.parse_args()
    
    # Determining option price
    if args.method == None:
         parser.error('Method of Option Pricing is required (Black Scholes, Binomial European or American, Monte Carlo Estimation)')
    if args.type == None:
         parser.error("Type of Option is missing (Call or Put)")
    if args.S == None or args.K == None or args.T == None or args.r == None or args.sigma == None or args.q == None:
        parser.error("Missing some value (try --help)")
    if args.method == "black_scholes":
        if args.type == "Call":
            option_price = BSCall(args.S, args.K, args.q, args.r, args.sigma, args.T)
        elif args.type == "Put":
            option_price = BSPut(args.S, args.K, args.q, args.r, args.sigma, args.T)
    elif args.method == "binomial_european":
        if args.n == None:
            parser.error("--n is required for Binomial European method")
        if args.type == "Call":
            option_price = bm_european(args.S, args.K, args.q, args.r, args.sigma, args.T, args.n, args.type)
        elif args.type == "Put":
                option_price = bm_european(args.S, args.K, args.q, args.r, args.sigma, args.T, args.n, isCall = False)
    elif args.method == "binomial_american":
        if args.n == None:
            parser.error("--n is required for Binomial American method")
        if args.type == "Call":
            option_price = bm_american(args.S, args.K, args.q, args.r, args.sigma, args.T, args.n, args.type)
        elif args.type == "Put":
                option_price = bm_american(args.S, args.K, args.q, args.r, args.sigma, args.T, args.n, isCall = False)
    elif args.method == "monte_carlo":
        if args.basic_anti == None or args.num == None:
            parser.error("Must specify basic estimation or antithetic estimation, as well as number of simulations")
        if args.basic_anti == "Basic":
            if args.type == "Call":
                option_price = mc(args.S, args.K, args.q, args.r, args.sigma, args.T, args.num)[0]
            elif args.type == "Put":
                option_price = mc(args.S, args.K, args.q, args.r, args.sigma, args.T, args.num, Call    = False)[0]
        elif args.basic_anti == "Antithetic":
            if args.type == "Call":
                    option_price = mc(args.S, args.K, args.q, args.r, args.sigma, args.T, args.num, Antithetic = True)[0]
            elif args.type == "Put":
                    option_price = mc(args.S, args.K, args.q, args.r, args.sigma, args.T, args.num, Antithetic = True)[0]

    print(f"{args.method.capitalize()} Option Price: {option_price:.2f}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')