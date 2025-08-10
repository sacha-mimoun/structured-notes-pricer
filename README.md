# Structured Notes Pricer

A Python-based pricing engine for structured products such as **Phoenix** and **Athena** notes.  
The framework simulates payoff profiles, computes fair values, and supports scenario analysis using configurable market data.

## Features
- **Phoenix note pricing** (autocallable with memory coupons)
- Modular design for adding new products (**Athena**, **BRC**, etc.)
- **Monte Carlo simulations** for path-dependent instruments
- Flexible market configuration (spot, volatility, interest rates)
- Clean, extensible codebase for advanced **quantitative finance** research and structured product analytics

## Example — Phoenix Note Pricing
```bash
python -m scripts.run_pricer
```
**Output:**
```
Prix théorique du Phoenix : 973,784.39
```

---

📂 Designed for transparency, reproducibility, and rapid prototyping of structured product pricing models.
