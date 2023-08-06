#!/usr/bin/env python3
'''Slightly more advanced example which requires "pip install bitmex-ws" to run. The data is pushed from the BitMEX server
   to our chart, which we update in a couple of Hertz.'''

from bitmex_websocket import Instrument
from bitmex_websocket.constants import InstrumentChannels
import copy
import finplot as fplt
import numpy as np
import pandas as pd
from threading import Thread


plot = None
raw_orderbook = None
gfx_orderbook = None
keep_seconds = 3
hz = 5
ws = Instrument(channels=[InstrumentChannels.orderBook10])


@ws.on('action')
def action(message):
    for orderbook10 in message['data']:
        try:
            ask = pd.DataFrame(orderbook10['asks'], columns=['price','volume'])
            bid = pd.DataFrame(orderbook10['bids'], columns=['price','volume'])
            ask['volume'] = ask['volume'].cumsum()
            bid['volume'] = bid['volume'].cumsum()
            bid['price'] -= 0.5
            global raw_orderbook, gfx_orderbook
            ask_price = ask.price[0]-0.25
            this_orderbook = pd.concat([bid.iloc[::-1], ask]).reset_index(drop=True)
            this_orderbook['live'] = keep_seconds*hz
            if raw_orderbook is not None:
                prev_orderbook = raw_orderbook.set_index('price')
                this_orderbook = this_orderbook.set_index('price')
                prev_orderbook['volume'] = np.nan
                this_orderbook = pd.concat([prev_orderbook, this_orderbook], axis=1)
                this_orderbook.iloc[this_orderbook.iloc[:,2]>-1, 0:1+1] = this_orderbook.iloc[:,2:3+1]
                this_orderbook = this_orderbook.iloc[:, 0:1+1].reset_index()
                missing_prices = set(np.arange(this_orderbook.price.min(), this_orderbook.price.max()+0.5, 0.5)) - set(this_orderbook.price)
                missing = pd.DataFrame([[mp,np.nan,0] for mp in missing_prices], columns='price volume live'.split())
                this_orderbook = pd.concat([this_orderbook, missing], axis=0).sort_values('price').reset_index(drop=True)
                this_orderbook.loc[this_orderbook.price<ask_price,'volume'] = this_orderbook.loc[this_orderbook.price<ask_price,'volume'].bfill()
                this_orderbook.loc[this_orderbook.price>ask_price,'volume'] = this_orderbook.loc[this_orderbook.price>ask_price,'volume'].ffill()
            this_orderbook.ask_price = ask_price
            raw_orderbook = gfx_orderbook = this_orderbook
        except Exception as e:
            print(type(e), e)


def update_plot():
    global plot, raw_orderbook, gfx_orderbook
    if gfx_orderbook is None:
        return
    ob = gfx_orderbook
    ask_idx = len(ob.loc[ob.price<ob.ask_price, :])
    cfun = fplt.volume_colorfilter_section([(0,'bull'),(ask_idx,'bear')])
    if plot is None:
        plot = fplt.bar(ob[['price','volume']], width=1, colorfunc=cfun)
        plot.x_offset = 0.5
    else:
        plot.colorfunc = cfun
        ob['live'] -= 1
        obf = ob.loc[ob.live>0].reset_index(drop=True)
        if len(obf):
            obf.ask_price = ob.ask_price
            raw_orderbook = obf
        if ob.live.max() >= keep_seconds*hz-1:
            plot.update_data(ob[['price','volume']])
            r = copy.deepcopy(plot.ax.vb.state['targetRange'])
            plot.ax.setLimits(xMin=0)
            r[0][1] = len(ob)
            plot.ax.vb.setRange(fplt.QtCore.QRectF(fplt.pg.Point(r[0][0], r[1][0]), fplt.pg.Point(r[0][1], r[1][1])), padding=0)
            if fplt.master_data[fplt.windows[-1]]['last_mouse_evs']:
                pos = fplt.master_data[fplt.windows[-1]]['last_mouse_evs'][-1]
                point = plot.ax.vb.mapSceneToView(pos)
                plot.ax.crosshair.update(point)


thread = Thread(target=ws.run_forever)
thread.daemon = True
thread.start()

ax = fplt.create_plot(maximize=False)
fplt.timer_callback(update_plot, 1/hz)
fplt.show()
