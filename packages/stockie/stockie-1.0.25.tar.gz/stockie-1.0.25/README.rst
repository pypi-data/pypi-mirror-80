Stockie
=======

a stock screener to help the stock traders in making a trading decisions. 

Feature in Stockie 1.0
====================== 

* **Multiple stock input**, This version allows multiple inputs for stock to be analyzed or displayed later.  
* **Tabular of candlestick detector**, you can show the table that shows whether a specific candlestick pattern has formed or not, with totally more than 50 patterns.
* **Interactive Candlestick stock screener**, an interactive HTML display of stock in candlestick.
* **Happening Pattern**, a table that show the currenly happening  pattern in last 10 days with it's accuracy based on the past and number their occurance. 

Setup
=====

Installing
~~~~~~~~~~

.. code:: python

	!pip install stockie


Import
~~~~~~

.. code:: python

	from Stockie.stockie import stockie

Utilization
===========

Load in stock name
~~~~~~~~~~~~~~~~~~
To load in the data, We use `yfinance <https://pypi.org/project/yfinance/>`_ package which is included inside. So, the input just nned to be the ticker of the stock which is registered.

.. code:: python

	a = stockie(['UNVR.JK','AAPL','AMZN.BA'])


Display tabular data
~~~~~~~~~~~~~~~~~~~~

.. code:: python

	df = a.find_pattern()['AAPL']


Stock screener
~~~~~~~~~~~~~~

.. code:: python

	a.get_candlestick_report()





, 