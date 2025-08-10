from src.products.phoenix import Phoenix
from src.market.market_data import MarketData

if __name__ == "__main__":
    # Paramètres marché (exemple)
    market = MarketData(spot=100.0, volatility=0.25, rate=0.02, dividend_yield=0.00)

    # Paramètres produit Phoenix (exemple)
    product = Phoenix(
        notional=1_000_000,
        strike=100.0,
        barrier=60.0,
        coupon=0.08,          # 8% annuel
        maturity_years=1.0,   # 1 an pour aller vite sur la démo
        freq_per_year=12      # observations mensuelles
    )

    price = product.price(market)
    print(f"Prix théorique du Phoenix : {price:.2f}")
