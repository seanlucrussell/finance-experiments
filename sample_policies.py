#!/bin/python3

# hide yfinance pandas warning until bugfix hist prod - see https://github.com/ranaroussi/yfinance/issues/1837
import warnings
warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated and will be removed in a future version. Use pd.to_timedelta instead.", category=FutureWarning, module="yfinance.utils")

import yfinance as yf
from backtesting_framework import register_policy, display_policy_backtest_result, compare_registered_policies

@register_policy("Always buy")
def buy_policy(policy_lower_bound, policy_upper_bound, history):
    return 1

@register_policy("Buy more")
def buy_more(policy_lower_bound,policy_upper_bound,history):
    return min(50,policy_upper_bound)

@register_policy("So greedy")
def greedy(policy_lower_bound,policy_upper_bound,history):
    return policy_upper_bound

@register_policy("Buy the dip")
def buy_low_sell_high(policy_lower_bound, policy_upper_bound, history):
    yesterday = history.tail(1)
    price_movement = yesterday['Close'].iat[0] - yesterday['Open'].iat[0]
    if price_movement > 0:
        return -1
    elif price_movement < 0:
        return 1
    return 0

@register_policy("Follow the hype")
def buy_high_sell_low(policy_lower_bound, policy_upper_bound, history):
    yesterday = history.tail(1)
    price_movement = yesterday['Close'].iat[0] - yesterday['Open'].iat[0]
    if price_movement > 0:
        return 1
    elif price_movement < 0:
        return -1
    return 0


ticker = yf.Ticker('XOM')
ticker_history = ticker.history(period='max')

initial_cash = 100
initial_holdings = 0

# display_policy_backtest_result(100,0,ticker_history,greedy)
compare_registered_policies(initial_cash, initial_holdings, ticker_history)
