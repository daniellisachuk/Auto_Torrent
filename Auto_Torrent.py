#!/usr/bin/env python

'''
requires transmission web client to be active
(transmission-gtk -> edit -> preferences -> remote(tab) -> allow remote access(enable))
'''

import os
import logging
import argparse
import transmissionrpc as trans
from crontab import CronTab


def resolve_args():
    # get and parse arguments
    parser = argparse.ArgumentParser(
        prog='AuToMan',
        description='Auto Torrent Manager',
        epilog='Created by Daniel Lisachuk as a leisure project / coding challenge'
    )
    parser.add_argument('-NDBUG',
                        action='store_true',
                        dest='debug',
                        help='Used for DEBUGGING purposes')
    subpursers = parser.add_subparsers(help='Commands')
    # The ADD Command
    ADD_parser = subpursers.add_parser('add', help='Add new Series to be Downloaded')
    ADD_parser.add_argument('Series',
                            help='Name of the Series to be Downloaded')
    ADD_parser.add_argument('day',
                            choices=('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'),
                            help='Set Day of New Episode Release')
    # The GET Command
    GET_parser = subpursers.add_parser('get', help='Download the specified Episode of specified Series')
    GET_parser.add_argument('Series',
                            help='Name of the Series to be Downloaded')
    GET_parser.add_argument('-s',
                            type=int,
                            dest='season',
                            help='Number of the Season to be Downloaded')
    GET_parser.add_argument('-e', type=int, dest='episode',
                            help='Number of the Episode to be Downloaded')
    # The LIST Command
    LIST_parser = subpursers.add_parser('list', help='List all monitored Series')
    LIST_parser.add_argument('-l', dest='long_listing',
                             action='store_true',
                             help='Long Listing Format')
    args = parser.parse_args()
    return args


def add_to_cron(series, relese_day):
    if debugging:
        print("adding {} to cron on {}".format(series, relese_day))

    cron = CronTab(user=True)

    for job in cron:
        if series in job.command:
            print('Series {} Already Exists'.format(series))
            return

    command = 'automan get "{}"'.format(series)
    comment = 'AuToMan - {} New Episode on {}'.format(series, relese_day)

    if debugging:
        print('Scheduling New Cron Job\nCommand is {}\nComment is {}'.format(command, comment))

    new_job = cron.new(command=command, comment=comment)
    new_job.minute.on(30)
    new_job.hour.on(21)
    new_job.dow.on(relese_day.upper())

    if debugging:
        print(str(new_job))

    # TODO implement a add-to-db func and call it here

    if debugging:
        print(str(cron))

    cron.write()


def download_next_episode():
    if debugging:
        print("downloading next episode")


'''
    -open selenium(firefox)/ beautiful soup(browser-less)
    -go to rarbg with args (will be provided by cron)
        # format is 'https://rarbgtor.org/torrents.php?search=final+space+s02+e03&category%5B%5D=41'
        # tokenize series argument and form a request separating words with '+' (for token in tokens: ...)
        ## category = 'TV HD Episodes'
    -   
'''


def download_specific_episode(series, season, episode):
    if debugging:
        print("downloading specific episode")


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


def list_monitored_series(ll):
    if debugging:
        if ll:
            print("listing monitored series in long listing mode")
        else:
            print("listing monitored series")


def download_season(Sreies, season):
    pass


def main():
    global debugging

    args = resolve_args()

    # TODO implement logger with basic level
    debugging = True  # TODO WHEN FINISHED CHANGE BACK TO : args.debug
    # debug massage
    if debugging:
        print(args.__dict__)
        # TODO set implemented logger to DEBUG level
    # if adding a new series
    if 'day' in args.__dict__:
        add_to_cron(args.Series, args.day)

    # if downloading an episode
    elif 'season' in args.__dict__:
        # if manual input #
        # - if all data is ok -- download specific episode
        if args.episode is not None and args.season is not None:
            download_specific_episode(args.Series, args.season, args.episode)

        # - if missing episode -- download whole season
        if args.episode is None and args.season is not None:
            download_season(args.Sreies, args.season)

        # - if missing season
        if args.episode is not None and args.season is None:
            print('Manual Mode Error: Missing Season No.')

        #  - if auto download
        if args.episode is None and args.season is None:
            download_next_episode(args.Series)  # auto download next episode in line TODO SERIES-SEASON-EPISODE DATABASE

    # if listing all series
    elif 'long_listing' in args.__dict__:
        list_monitored_series(args.long_listing)

    print('Exiting...')
    print('Good Bye...')


if __name__ == '__main__':
    main()

