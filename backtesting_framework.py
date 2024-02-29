#!/bin/python3

policies = []

def register_policy(policy_name):
    def wrap(f):
        policies.append((policy_name,f))
        return f
    return wrap

def backtest(initial_cash, initial_holdings, ticker_history, policy):
    cash = initial_cash
    holdings = initial_holdings

    result = []
    for i in range(len(ticker_history)):
        current_history = ticker_history.head(i+1)
        yesterday = current_history.tail(1)
        price = yesterday['Close'].iat[0]
        policy_lower_bound = -holdings
        policy_upper_bound = int(cash // price)
        policy_decision = policy(policy_lower_bound,policy_upper_bound,current_history)
        cash += holdings * yesterday['Dividends'].iat[0]
        if policy_lower_bound <= policy_decision <= policy_upper_bound:
            holdings += policy_decision
            cash -= policy_decision * price
        assert holdings >= 0
        assert cash >= 0
        net_worth = price * holdings + cash
        yesterdays_date = list(yesterday.index)[0].date().strftime('%Y-%m-%d')
        row = { 'date': yesterdays_date, 'holdings': holdings, 'cash': cash,
                'net_worth' : net_worth}
        result.append(row)
    return result

def print_row(row):
    date = row['date']
    holdings = row['holdings']
    cash = row['cash']
    net_worth = row['net_worth']
    print(f'{date}:   Own {holdings:>14,} shares,   Cash ${cash:>20,.2f},   Net worth ${net_worth:>22,.2f}')


def display_policy_backtest_result(initial_cash, initial_holdings, ticker_history, policy):
    for row in backtest(initial_cash,initial_holdings,ticker_history,policy):
        print_row(row)

def compare_registered_policies(initial_cash, initial_holdings, ticker_history):
    for name,policy in policies:
        print(name)
        result = backtest(initial_cash,initial_holdings,ticker_history,policy)[-1]
        print_row(result)
