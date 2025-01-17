#%% Imports

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

url='https://www.fxcorporate.com/Hosts.jsp'
connection='Demo'
quotes_count='800'
"""

def parse_args():
    parser = argparse.ArgumentParser(description='Process command parameters.')
    #jgtcomm.add_main_arguments(parser)
    jgtcomm.add_instrument_timeframe_arguments(parser)
    #common_samples.add_date_arguments(parser)
    jgtcomm.add_tlid_range_argument(parser)
    #jgtcomm.add_date_arguments(parser)
    jgtcomm.add_max_bars_arguments(parser)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    str_user_id = user_id#args.l
    str_password = password#args.p
    str_url = url#args.u
    
    if args.tlidrange is not None:
      tlid_range = args.tlidrange
      #print(tlid_range)
      dtf,dtt = jgtcomm.tlid_range_to_start_end_datetime(tlid_range)
      #print(str(dtf) + " " + str(dtt))
      date_from =dtf
      date_to = dtt
      
    str_connection = connection#args.c
    #str_session_id = args.session
    #str_pin = args.pin
    
    str_instrument = args.instrument
    str_timeframe = args.timeframe
    quotes_count = args.quotescount

    with ForexConnect() as fx:
        try:
            fx.login(str_user_id, str_password, str_url,
                     str_connection,
                     common_samples.session_status_changed)

            #print("")
            #print("Requesting a price history...")
            history = fx.get_history(str_instrument, str_timeframe, date_from, date_to, quotes_count)
            current_unit, _ = ForexConnect.parse_timeframe(str_timeframe)
           
            date_format = '%m.%d.%Y %H:%M:%S'
            date_format = '%Y-%d-%m %H:%M:%S'
            if current_unit == fxcorepy.O2GTimeFrameUnit.TICK:
                print("Date, Bid, Ask")
                print(history.dtype.names)
                for row in history:
                    print("{0:s}, {1:,.5f}, {2:,.5f}".format(
                        pd.to_datetime(str(row['Date'])).strftime(date_format), row['Bid'], row['Ask']))
            else:
                print("Date, Open, High, Low, Close, Median, Volume")
                for row in history:
                    open_price = (row['BidOpen'] + row['AskOpen']) / 2
                    high_price = (row['BidHigh'] + row['AskHigh']) / 2
                    low_price = (row['BidLow'] + row['AskLow']) / 2
                    close_price = (row['BidClose'] + row['AskClose']) / 2
                    median = (high_price + low_price) / 2
                    print("{0:s},{1:.5f},{2:.5f},{3:.5f},{4:.5f},{5:.5f},{6:d}".format(
                        pd.to_datetime(str(row['Date'])).strftime(date_format), open_price, high_price,
                        low_price, close_price, median, row['Volume']))
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
