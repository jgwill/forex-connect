# Copyright 2019 Gehtsoft USA LLC

# Licensed under the license derived from the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.

# You may obtain a copy of the License at

# http://fxcodebase.com/licenses/open-source/license.html

# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import pandas as pd
from forexconnect import ForexConnect, fxcorepy
#from jgtpy import JGTConfig as conf

from dotenv import load_dotenv
from dotenv import dotenv_values
import os
load_dotenv()  # take environment variables from .env.
#env=load_dotenv(os.getenv(os.getcwd()))
env = dotenv_values(".env")

if os.getenv('user_id') == "":
  load_dotenv(os.getenv('HOME'))
if os.getenv('user_id') == "":
  load_dotenv(os.getenv(os.getcwd()))
user_id = os.getenv('user_id')
password = os.getenv('password')
url = os.getenv('url')
connection = os.getenv('connection')
quotes_count = os.getenv('quotes_count')

from jgtpy import jgtcommon as jgtcomm
import common_samples
"""

user_id='U10D2459770'
password='Oz4pb'
url='https://www.fxcorporate.com/Hosts.jsp'
connection='Demo'
quotes_count='800'
"""

def parse_args():
    parser = argparse.ArgumentParser(description='Process command parameters.')
    #jgtcomm.add_main_arguments(parser)
    jgtcomm.add_instrument_timeframe_arguments(parser)
    jgtcomm.add_date_arguments(parser)
    jgtcomm.add_max_bars_arguments(parser)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    str_user_id = user_id#args.l
    str_password = password#args.p
    str_url = url#args.u
    str_connection = connection#args.c
    #str_session_id = args.session
    #str_pin = args.pin
    
    str_instrument = args.instrument
    str_timeframe = args.timeframe
    quotes_count = args.quotescount
    date_from = args.datefrom
    date_to = args.dateto

    with ForexConnect() as fx:
        try:
            fx.login(str_user_id, str_password, str_url,
                     str_connection,
                     common_samples.session_status_changed)

            print("")
            print("Requesting a price history...")
            history = fx.get_history(str_instrument, str_timeframe, date_from, date_to, quotes_count)
            current_unit, _ = ForexConnect.parse_timeframe(str_timeframe)
           
            date_format = '%m.%d.%Y %H:%M:%S'
            if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
                print("Date, Bid, Ask")
                print(history.dtype.names)
                for row in history:
                    print("{0:s}, {1:,.5f}, {2:,.5f}".format(
                        pd.to_datetime(str(row['Date'])).strftime(date_format), row['Bid'], row['Ask']))
            else:
                print("Date, BidOpen, BidHigh, BidLow, BidClose, Volume")
                for row in history:
                    print("{0:s}, {1:,.5f}, {2:,.5f}, {3:,.5f}, {4:,.5f}, {5:d}".format(
                        pd.to_datetime(str(row['Date'])).strftime(date_format), row['BidOpen'], row['BidHigh'],
                        row['BidLow'], row['BidClose'], row['Volume']))
        except Exception as e:
            jgtcomm.print_exception(e)
        try:
            fx.logout()
        except Exception as e:
            jgtcomm.print_exception(e)


if __name__ == "__main__":
    main()
    print("")
    #input("Done! Press enter key to exit\n")
