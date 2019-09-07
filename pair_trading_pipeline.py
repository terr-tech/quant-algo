from quantopian.pipeline.data import morningstar
from quantopian.pipeline.classifiers.morningstar import Sector

morningstar_sector = Sector()
morningstar_sector
exchange = morningstar.share_class_reference.exchange_id.latest
exchange
#the exchange here is a classifier
#no use unless we build filters with it
#create a new filter for just new york stock exchange
nyse_filter = exchange.eq("NYS")


#purpose of this file is to make pipelines
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import SimpleMovingAverage

SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 30)

def make_pipeline():
    
    latest_close = USEquityPricing.close.latest
    small_price = latest_close < 5
    
    #classifier:
    #creates a filter to show only stocks listed on new york stock exchange.
    nyse_filter = exchange.eq("NYS")
    
    mean_close_30 = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 30, mask = small_price)
    mean_close_10 = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 10, mask = small_price)
    #*please note the mask. it is applied in simple moving average for the reason of saving computational
    #efforts
    
    percent_diff = (mean_close_10 - mean_close_30)/mean_close_30
    perc_filter = percent_diff > 0
    
    
    #final filter:
    final_filter = perc_filter & small_price &nyse_filter
    
    return Pipeline(columns = {'30 Day Mean Close': mean_close_30,
                               'Percent Diff': percent_diff,
                              'Latest Close': latest_close,
                              'Percent Filter': perc_filter}, screen = final_filter)
results = run_pipeline(make_pipeline(), '2019-09-03', '2019-09-03')

#check and see:
results.head()
results.info()
