#!/usr/bin/env python3

import finplot as fplt
import yfinance


df = yfinance.download('TSLA', '2020-07-30', interval='60m')

ax = fplt.create_plot('Tesla rocks')
fplt.candlestick_ochl(df[['Open','Close','High','Low']])

x0 = len(df)-12
x = [x0-0.2, x0+0.1, x0+0.3]
y0 = df.Close.iloc[-12]
y = [y0+0.1, y0+2.7, y0+7.9]
ds = fplt._create_datasrc(ax, x, y)
ds.standalone = True
fplt.plot(ds, style='>', width=2)

fplt.show()
