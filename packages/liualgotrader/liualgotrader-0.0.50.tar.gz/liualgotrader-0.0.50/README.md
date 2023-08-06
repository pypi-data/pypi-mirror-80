# LiuAlgoTrader
[![Build Status](https://travis-ci.org/amor71/LiuAlgoTrader.svg?branch=master)](https://travis-ci.org/amor71/LiuAlgoTrader)
[![Python 3](https://pyup.io/repos/github/amor71/LiuAlgoTrader/python-3-shield.svg)](https://pyup.io/repos/github/amor71/LiuAlgoTrader/)
[![Updates](https://pyup.io/repos/github/amor71/LiuAlgoTrader/shield.svg)](https://pyup.io/repos/github/amor71/LiuAlgoTrader/)
[![Documentation Status](https://readthedocs.org/projects/liualgotrader/badge/?version=latest)](https://liualgotrader.readthedocs.io/en/latest/?badge=latest)

## Introduction

**LiuAlgoTrader** is a Pythonic all-batteries-included framework
for effective algorithmic trading. The framework is
intended to simplify development, testing,
deployment and evaluating algo trading strategies.

LiuAlgoTrader can run on a Macbook laptop and 
*hedge-on-the-go*, or run on a multi-core hosted Linux server 
and it will optimize for best performance for either. 

LiuAlgoTrader is Work-In-Progress, however it is a fully
functional and powerful framework that may be used almost out-of-the-box.
Assistance in development is highly appreciated,
as well as comments and suggestions. Please check the
Contribution section for further details.

## Quickstart

Read the below, or use [the docker implementations](https://github.com/amor71/trade_deploy). 

### Prerequisite

- Paper, and preferable a funded Live account with [Alpaca Markets](https://alpaca.markets/docs/about-us/).
- Installed [PostgreSQL](https://www.postgresql.org/) database (or see *Alternative Installation* below)

### Installation

To install LiuAlgoTrader just type:

`pip install liualgotrader`

**Note** if you're running on Windows, TA-LIB setup might fail, in which case try https://github.com/mrjbq7/ta-lib#troubleshooting, and re-try installing the `liualgotrader` package.
 
#### Alternative Installation 

liualgotrader requires several packages to be properly installed, as well as a PostgrSQL database properly configured. For first time users, it might be easier to install the docker version https://github.com/amor71/trade_deploy .

### First time run

LiuAlgoTrader applications require some 
configuration and setup which are best described 
in the documentation. However, to confirm your 
installation just type:

`trader`

## Documentation

Is available [here](https://liualgotrader.readthedocs.io/en/latest/).

## Samples

Can we found in the [examples](examples) directory. 

## Development

Would you like to help me complete & evolve LiuAlgoTrader? 
Do you have a suggestion, comment, idea for improvement or 
a have a wish-list item? Don't be shy and email me at 
amichay@sgeltd.com


