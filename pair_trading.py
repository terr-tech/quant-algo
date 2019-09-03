#This simple algorithm explains pair trading in quantitative finance
#it is used when we have 2 stocks that are similar in price movements


import numpy as np

#initializing our trading algorithm
def initialize(context):

    #create a schedule function for everyday + market close
    schedule_function(check_pairs, date_rules.every_day(),
    time_rules.market_close(minutes=60))

    #setting our context aa to american airline
    context.aa = sid(45971)

    #setting our context ual to united airline
    context.ual = sid(28051)


    context.long_on_spread = False
    context.shorting_spread = False

def check_pairs(context, data):
    #old code that can be reused:
    #tech_close = data.current(context.techies, 'close')
    #print(tech_close)
    #order_target_percent(context.aapl,.27)
    #order_target_percent(context.csco,.20)
    #order_target_percent(context.amzn,.53)

    #alias
    aa = context.aa
    ual = context.ual

    #set historic prices
    prices = data.history([aa,ual], 'price', 30, '1d')

    #today's prices
    short_prices = prices.iloc[-1:]


    #spread (moving average)
    mavg_30 = np.mean(prices[aa] - prices[ual])

    #standard deviation
    std_30 = np.std(prices[aa] - prices[ual])

    mavg_1 = np.mean(short_prices[aa] - short_prices[ual])

    #algorithm begins:
    if std_30 > 0:

        #calculate the z-score, then normalize this
        zscore = (mavg_1 - mavg_30)/std_30


        if zscore > 0.5 and not context.shorting_spread:

            #SPREAD = AA - UAL
            #shorting american airline stock
            order_target_percent(aa, -0.5)
            order_target_percent(ual, 0.5)
            context.shorting_spread = True
            context.long_on_spread - False


        elif zscore < 1.0 and not context.long_on_spread:

            order_target_percent(aa, 0.5)
            #shorting united airline stock
            order_target_percent(ual, -0.5)
            context.shorting_spread = False
            context.long_on_spread = True

        #if my zscore is 0 to 0.1, just clear it
        elif abs(zscore) < 0.1:
            order_target_percent(aa, 0)
            order_target_percent(ual, 0)
            context.shorting_spread = False
            context.long_on_spread = False

        #record for visualization
        record(Z_score = zscore)
