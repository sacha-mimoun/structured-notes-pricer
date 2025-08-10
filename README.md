# Structured Notes Pricer
A Python–based pricer for structured products such as **Phoenix** and **Athena** notes.  
The project simulates payoff profiles, estimates fair value, and allows scenario analysis using market data.

## Features
- Pricing of **Phoenix notes** (autocallable with memory coupons)
- Modular architecture for adding other structured products (Athena, BRC, etc.)
- Monte Carlo simulations for path-dependent products
- Configurable market parameters (spot, volatility, interest rates)
- Modular, production-grade codebase built for advanced quantitative research and structured product analytics
## Example: Phoenix Note Pricing
```bash
python -m scripts.run_pricer

Output:
Prix théorique du Phoenix : 973,784.39
```
