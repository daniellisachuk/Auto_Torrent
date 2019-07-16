#!/usr/bin/env python

'''
requires transmission web client to be active
(transmission-gtk -> edit -> preferences -> remote(tab) -> allow remote access(enable))
'''

import os
import logging
import argparse



def add_to_cron():
    if debugging:
        print("adding to cron")
    from crontab import CronTab


def download_next_episode():
    pass


'''
    -open selenium(firefox)/ beautiful soup(browser-less)
    -go to rarbg with args (will be provided by cron)
        # format is 'https://rarbgtor.org/torrents.php?search=final+space+s02+e03&category%5B%5D=41'
        # tokenize series argument and form a request separating words with '+' (for token in tokens: ...)
        ## category = 'TV HD Episodes'
    -
'''


def find_and_download():
    if debugging:
        print("finding and downloading")

    import transmissionrpc as trans

    # # simple way to run transmission in background for http client (needed anyway)
    # # TODO IMPLEMENT BY FORKING
    # # get forked pid
    # # use exec(lv?? [one of them]) to run the command:
    # os.system("transmission-gtk -m")
    #
    # # works
    # client = trans.Client('localhost', port=9091)
    # client.get_torrents()
    #
    # # haven't tried yet
    # client.add_torrent()
    #
    # # TODO KILL FORKED TRANSMISSION-GTK BY PID (AND WAIT FOR IT?[BY PROC.WAIT? BY TIME.SLEEP?])


def list_monitored_series():
    if debugging:
        print("listing monitored series")


# get and parse arguments
parser = argparse.ArgumentParser(
    prog='AuToMan',
    description='Auto Torrent Manager',
    epilog='Created by Daniel Lisachuk as a leisure project / code challenge'
)

parser.add_argument('Series',
                    help='Name of the Series to be Downloaded')

parser.add_argument('-NDBUG', action='store_true', dest='debug',
                    help='Used for DEBUG purposes')

subpursers = parser.add_subparsers(help='Commands')

# The ADD Command
ADD_parser = subpursers.add_parser('add', help='Add new Series to be Downloaded')
ADD_parser.add_argument('-d', choices=('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'), dest='day',
                        help='Set Day of New Episode Release')

# The GET Command
GET_parser = subpursers.add_parser('get', help='Download the specified Episode of specified Series')
GET_parser.add_argument('-s', type=int, dest='season',
                        help='Number of the Season to be Downloaded')
GET_parser.add_argument('-e', type=int, dest='episode',
                        help='Number of the Episode to be Downloaded')

# The LIST Command
LIST_parser = subpursers.add_parser('list', help='List all monitored Series')
LIST_parser.add_argument('-l', dest='long_listing', action='store_true',
                         help='Long Listing Format')
args = parser.parse_args()

# TODO implement logger with basic level

debugging = True  # TODO WHEN FINISHED CHANGE BACK TO : args.debug

# debug massage
if debugging:
    print(args.__dict__)
    # TODO implement logger DEBUG level

# if adding a new series
if 'day' in args.__dict__:
    add_to_cron()

# if downloading an episode
elif 'episode' in args.__dict__:
    # if manual input #
    # - if all data is ok
    if args.episode is not None and args.season is not None:
        find_and_download(args.season, args.episode)

    # - if only missing episode
    if args.episode is None and args.season is not None:
        print('Manual Mode Error: Missing Episode No.')

    # - if only missing season
    if args.episode is not None and args.season is None:
        print('Manual Mode Error: Missing Season No.')

    # if auto download #
    if args.episode is None and args.season is None:
        download_next_episode()  # auto download next episode in line TODO SERIES-SEASON-EPISODE DATABASE

# if listing all series
elif 'long_listing' in args.__dict__:
    list_monitored_series()

