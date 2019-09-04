
#purpose of this file is to make pipelines
from quantopian.pipeline import Pipeline
from quantopian.research import run_pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import SimpleMovingAverage

def make_pipeline():
    mean_close_30 = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 30)
    mean_close_10 = SimpleMovingAverage(inputs = [USEquityPricing.close], window_length = 10)
    latest_close = USEquityPricing.close.latest

    percent_diff = (mean_close_10 - mean_close_30)/mean_close_30

    return Pipeline(columns = {'30 Day Mean Close': mean_close_30,
                               'Percent Diff': percent_diff,
                              'Latest Close': latest_close})
results = run_pipeline(make_pipeline(), '2019-09-03', '2019-09-03')
results.head()
