class MarketData:
    def __init__(self, spot: float, volatility: float, rate: float, dividend_yield: float = 0.0):
        self.spot = spot
        self.volatility = volatility
        self.rate = rate
        self.dividend_yield = dividend_yield
