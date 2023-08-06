# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oanda_chart',
 'oanda_chart.env',
 'oanda_chart.selectors',
 'oanda_chart.util',
 'oanda_chart.widgets']

package_data = \
{'': ['*'], 'oanda_chart': ['geo/*', 'image_data/*']}

install_requires = \
['forex-types>=0.0.6,<0.0.7',
 'oanda-candles>=0.1.0,<0.2.0',
 'tk-oddbox>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'oanda-chart',
    'version': '0.1.0',
    'description': 'Oanda forex candle chart tkinter widget.',
    'long_description': '# oanda-chart\nOanda forex candle chart tkinter widget.\n\n### Warning:\nThis package does not yet have all its core features, and even its\ncurrent features might change significantly.\n\nIt was uploaded to pypi.org early as an experiment to see if the package\ncould find some "png" after installation...not because it was at\nall ready.\n\n### Some Background\nThis is being built on top of oanda-candles package which is built\non top of the oandaV20 package, which uses the Oanda Restful API.\n\nIt provides a tkinter chart widget and associated widgets to select\nthe instrument pair, granularity, and ask/mid/bid.\n\n\n### Version Notes\n\n#### 0.1.0\nBig rework. Now has price and time scales. Changes include:\n\n1. Price scale, which can be stretched with mouse to make candles appear taller or shorter.\n1. Time scale, which can be stretched with the mouse to make candles wider or narrower, similar to mouse wheel.\n1. Both time and price grid lines aligning with scales.\n1. Badge in background declaring the instrument pair, granularity, and whether its bid, mid, or ask.\n1. Panning up or down will take one out of price view mode.\n1. When chart is in focus (which it becomes when panning it) user can use arrow keys on keyboard to move in chart.\n1. Enter key on keyboard snaps back to price view mode.\n1. In bottom right corner the pips between price grid lines and time interval between time grid lines is shown.\n1. Clicking this bottom right corner area snaps chart view back to the default way the chart was set when loaded.\n1. The user should not be able to tell, but the scrollable canvas area is now only three times bigger than the viewing area in all directions.\n1. Candle times are now aligned on UTC (for example monthly candles start right when the month changes in UTC)\n1. The time scale and time on the Candle objects are in UTC (and no longer local or New York time)\n1. Features have not been greatly tested, and code got a huge rewrite that could be cleaned up.\n\n###### Still Missing features\n1. No geometric annotation items like price lines or rectangles etc are implemented yet...but they are what is being looked at next.\n1. No configuration of colors is available yet--all colors are just hard coded with a darkish look.\n\n#### 0.0.4\nOverall, I think the core functionality is finally taking shape. Still seriously missing parts, particularly price scale on right and time scale on\n bottom. And there are no drawing utilities yet. What I am happy with is that panning around and candle display and such feel reasonably comparable to "real" candle charts used by retail brokers.\n Including niceness users expect without thinking, like scrunching candles with mouse wheel, and the candles following price when panning.\n \nThese features are currently working (keep warning in mind, things may change):\n\n\n1. Flag Pair Selector built in to standard chart by default\n1. Menu pull down Pair selector also built in.\n1. Granularity pull down as well.\n1. Quote Kind (bid/mid/ask) pull down as well.\n1. Supports making candles fatter or skinnier with mouse wheel.\n1. Supports panning around in two modes--to switch modes double-click.\n   1. Price View True: pulls back view up or down to current price and fits the current price action to the view size.\n   1. Price View False: user can pan anywhere including above and below prices.\n1. If panned so that latest candles are in view, will check for updated candle data every 2 seconds.\n1. Draws price grid lines behind candles based, but does NOT yet have a price scale telling you what prices they are.\n1. Does NOT yet have a time scale.\n1. Pair, Gran, and QuoteKind Selector classes have a color theme that links them together and they can be linked in theory to different charts. The idea is to allow changing the Pair in one chart change it in others as well. Also for granularity and quote kind. The color will be visible on the widgets so users know which are linked.\n\n\n\n',
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aallaire/oanda-chart',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
