import numpy as np

class Phoenix:
    """
    Phoenix simplifié pour démo :
    - Sous-jacent simulé en GBM
    - Coupons observés à fréquence fixe si S >= barrier (avec mémoire)
    - Autocall si S >= strike à une date d’observation
    - À maturité : si pas autocalled, coupon éventuel + remboursement
      Knock-in simplifié : si min(path) < barrier et ST < strike => notional * ST/strike
    """

    def __init__(
        self,
        notional: float,
        strike: float,
        barrier: float,
        coupon: float,          # ex: 0.08 = 8% annuel
        maturity_years: float,
        freq_per_year: int,
        memory: bool = True,
        n_paths: int = 50_000,
        seed: int | None = 42,
    ):
        self.notional = float(notional)
        self.strike = float(strike)
        self.barrier = float(barrier)
        self.coupon = float(coupon)
        self.maturity_years = float(maturity_years)
        self.freq_per_year = int(freq_per_year)
        self.memory = bool(memory)
        self.n_paths = int(n_paths)
        self.seed = seed

    def _simulate_paths(self, spot, vol, r, q):
        """Simulation GBM vectorisée (retourne S de forme (n_paths, steps+1))."""
        steps = int(self.maturity_years * self.freq_per_year)
        dt = 1.0 / self.freq_per_year
        rng = np.random.default_rng(self.seed)

        Z = rng.standard_normal((self.n_paths, steps))
        drift = (r - q - 0.5 * vol**2) * dt
        diff = vol * np.sqrt(dt)

        log_incr = drift + diff * Z
        log_paths = np.cumsum(log_incr, axis=1)
        S = spot * np.exp(np.hstack([np.zeros((self.n_paths, 1)), log_paths]))
        return S, steps, dt

    def price(self, market) -> float:
        S, steps, dt = self._simulate_paths(
            market.spot, market.volatility, market.rate, market.dividend_yield
        )
        obs_idx = np.arange(self.freq_per_year, steps + 1, self.freq_per_year)
        df = lambda t: np.exp(-market.rate * t)

        pv = np.zeros(self.n_paths)
        redeemed = np.zeros(self.n_paths, dtype=bool)
        missed = np.zeros(self.n_paths, dtype=int)  # mémoire de coupons

        min_on_path = S.min(axis=1)               # pour le knock-in
        has_knockin = min_on_path < self.barrier

        for k in obs_idx:
            if redeemed.all():
                break
            t = k * dt
            Sk = S[:, k]

            # Coupon si au-dessus de la barrière
            eligible = (Sk >= self.barrier) & (~redeemed)
            if eligible.any():
                nb = (missed[eligible] + 1) if self.memory else 1
                cpn = self.coupon / self.freq_per_year * self.notional * nb
                pv[eligible] += df(t) * cpn
                missed[eligible] = 0

            # Incrément de mémoire pour ceux qui n’ont pas touché
            inc_mask = (~eligible) & (~redeemed)
            missed[inc_mask] += 1

            # Autocall si au-dessus du strike
            ac = (Sk >= self.strike) & (~redeemed)
            if ac.any():
                pv[ac] += df(t) * self.notional
                redeemed[ac] = True

        # À maturité pour ceux non remboursés
        remain = ~redeemed
        if remain.any():
            tM = steps * dt
            ST = S[remain, -1]

            # Coupon final si éligible
            final_elig = ST >= self.barrier
            if final_elig.any():
                nb = (missed[remain][final_elig] + 1) if self.memory else 1
                cpn = self.coupon / self.freq_per_year * self.notional * nb
                pv[remain][final_elig] += df(tM) * cpn

            # Remboursement nominal vs proportionnel (knock-in)
            ki = has_knockin[remain] & (ST < self.strike)
            red = np.where(ki, self.notional * (ST / self.strike), self.notional)
            pv[remain] += df(tM) * red

        return float(np.mean(pv))
