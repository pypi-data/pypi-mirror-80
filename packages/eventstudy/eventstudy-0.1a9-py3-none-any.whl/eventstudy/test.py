import numpy as np
import matplotlib.pyplot as plt

from .single import Single
from .multiple import Multiple

Single.import_returns('returns_GAFAM.csv')
Single.import_FamaFrench('famafrench.csv')

event = Single.market_model(
    security_ticker = 'AAPL',
    market_ticker = 'SPY',
    event_date = np.datetime64('2007-01-09'),
    event_window = (-1,+1), 
    estimation_size = 300,
    buffer_size = 30
)

event.plot(AR=True)
plt.show()