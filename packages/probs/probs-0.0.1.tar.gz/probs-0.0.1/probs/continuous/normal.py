import math
from dataclasses import dataclass
from typing import cast

from probs.rv import RandomVariable


@dataclass
class Normal(RandomVariable):
    """
    The normal distribution is a type of continuous probability distribution
    for a real-valued random variable.

    https://en.wikipedia.org/wiki/Normal_distribution
    """

    mu: float = 0
    sigma: float = 1

    def __post_init__(self) -> None:
        self.sigma_sq = self.sigma ** 2

    def __str__(self) -> str:
        return f"Normal(μ={self.mu}, σ²={self.sigma_sq})"

    def __add__(self, other: object) -> RandomVariable:
        if isinstance(other, Normal):
            return Normal(self.mu + other.mu, math.sqrt(self.sigma_sq + other.sigma_sq))
        if isinstance(other, RandomVariable):
            return cast(RandomVariable, super().__add__(other))
        if isinstance(other, (int, float)):
            return Normal(self.mu + other, self.sigma)
        raise TypeError

    def __sub__(self, other: object) -> RandomVariable:
        if isinstance(other, Normal):
            return Normal(self.mu - other.mu, math.sqrt(self.sigma_sq + other.sigma_sq))
        if isinstance(other, RandomVariable):
            return cast(RandomVariable, super().__sub__(other))
        if isinstance(other, (int, float)):
            return Normal(self.mu - other, self.sigma)
        raise TypeError

    def __mul__(self, other: object) -> RandomVariable:
        if isinstance(other, (int, float)):
            return Normal(self.mu * other, self.sigma * (other ** 2))
        return cast(RandomVariable, super().__mul__(other))

    def __div__(self, other: object) -> RandomVariable:
        if isinstance(other, (int, float)):
            return self * (1.0 / other)
        return cast(RandomVariable, super().__div__(other))

    def expectation(self) -> float:
        return self.mu

    def variance(self) -> float:
        return self.sigma_sq

    def pdf(self, x: float) -> float:
        return (
            1
            / math.sqrt(2 * math.pi * self.sigma_sq)
            * math.exp(-((x - self.mu) ** 2) / (2 * self.sigma_sq))
        )

    def cdf(self, x: float) -> float:
        return 0
