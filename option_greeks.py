import numpy as np
import math
from scipy.stats import norm


class BlackScholesCalculator(object):
    def __init__(self, spot, strike, vol, rate, div, dte):
        self.spot_price = spot
        self.strike_price = strike
        self.volatility = vol / 100.0
        self.risk_free_rate = rate / 100.0
        self.annual_dividend_yield = div / 100.0
        self.days_to_expiry = dte / 365.0
        self.d1 = (
            ((np.log(self.spot_price / self.strike_price)) +
             self.days_to_expiry * (self.risk_free_rate - self.annual_dividend_yield +
                                    (pow(self.volatility, 2) / 2))) / (self.volatility * math.sqrt(self.days_to_expiry))
        )
        self.d2 = self.d1 - (self.volatility * math.sqrt(self.days_to_expiry))
        self.Nd1 = norm.cdf(self.d1)
        self.Nd1_negative = norm.cdf(-self.d1)
        self.Nd2 = norm.cdf(self.d2)
        self.Nd2_negative = norm.cdf(-self.d2)

    def call_option_price(self):
        return (self.spot_price * math.exp(-1 * self.annual_dividend_yield * self.days_to_expiry) * self.Nd1 -
                self.strike_price * math.exp(-1 * self.risk_free_rate * self.days_to_expiry) * self.Nd2)

    def put_option_price(self):
        return (self.strike_price * math.exp(-1 * self.risk_free_rate * self.days_to_expiry) * self.Nd2_negative -
                self.spot_price * math.exp(-1 * self.annual_dividend_yield * self.days_to_expiry) * self.Nd1_negative)


if __name__ == "__main__":
    # params: Spot price, strike price, volatility%, interest rate%, dividend yield annual%, DTE
    bs = BlackScholesCalculator(272.7, 280, 43.55, 7.4769, 0, 1)
    print "call option price: ", bs.call_option_price()
    print "put option _price: ", bs.put_option_price()
