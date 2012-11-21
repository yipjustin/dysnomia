import data
import math

def Run():
  market_date = data.GetDates()
  # artificial price
  spy_aprc = data.GetSPY()
  # can use other stock, e.g.
  #ko_aprc = data.GetKO()
  # aprc = data.GetPEP()
  # aprc = data.GetXLP()
  #RunStrategy(market_date, ko_aprc)
  RunStrategy(market_date, spy_aprc)


def GetReturnSeries(nav_list):
  return_series = []
  for i in range(len(nav_list)):
    if i == 0:
      return_series.append(0)
    else:
      return_series.append((nav_list[i] / nav_list[i-1]) - 1)
  return return_series


def Average(l):
  return sum(l) / len(l)


def Analyze(nav_list):
  # Make Return time series
  return_list = GetReturnSeries(nav_list)

  # Calculate return average
  average_return = Average(return_list)
 
  # Calculate return SD
  variance_list = [(r - average_return)**2 for r in return_list]
  return_sd = math.sqrt(Average(variance_list))
  
  # Calculate sharpe ratio
  trading_days = 252
  annual_return = math.pow(1 + average_return, trading_days) - 1
  annual_volatility = return_sd * math.sqrt(trading_days)
  
  # Sharpe
  sharpe = annual_return / annual_volatility

  results = {
      'return': annual_return,
      'volatility': annual_volatility,
      'sharpe': sharpe,
      }
  return results
      

def RunStrategy(market_date, aprc):
  # When SPY rises for 2 consecutive days, then long.
  # Exit when lower than previous day close.
  cash = 100000.0
  long_quantity = 0

  nav_history = []

  for i, d in enumerate(market_date):
    # Skip first two days.
    if i < 2:
      continue

    # Exit if lower than previous day close
    if aprc[i] < aprc[i-1] and long_quantity > 0:
      cash += long_quantity * aprc[i]
      long_quantity = 0

    # Enter if raised for two consecutive days
    if aprc[i] > aprc[i-1] and aprc[i-1] > aprc[i-2] and long_quantity == 0:
      long_quantity = cash / aprc[i]
      cash = 0

    # Book keeping
    nav = cash + long_quantity * aprc[i]
    nav_history.append(nav)
   
    # Print out result every 250 days
    if i % 250 == 0:
      print 'Date: %s, NAV: %f' % (d, nav)

  results = Analyze(nav_history)
  print 'Return: ', results['return']
  print 'Volatility: ', results['volatility']
  print 'Sharpe: ', results['sharpe']
  

if __name__ == '__main__':
  Run()
