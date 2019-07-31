#!/usr/bin/env python

# requires transmission web client to be active
# (transmission-gtk -> edit -> preferences -> remote(tab) -> allow remote access(enable))

import os
import logging
import argparse
import transmissionrpc as trans
from tinydb import TinyDB, Query
from crontab import CronTab
from tabulate import tabulate


# working with tinydb
#
# from tinydb import TinyDb, Query
#
# db = TinyDb('path/to/db.json')
# series = db.table('series')
# Serie = Query()
#
# # searching : returns a 'document'
#
# result = series.get(Serie.name == 'One Punch Man')
# will return a DICT representing the object labeled "1" below
#
# result = series.search(Serie.name == 'One Punch Man')
# will return a LIST containing the DICT representing the object labeled "1" below
#
# # accsessing fields :
# result['curr_season'/'curr_episode'/etc...]
#
# for list of episodes :
# result['available_episodes']['1'] will return [1, 2, 3, 4, 5, 6] from below
#
# # for writing back to db :
# resault.doc_id #will return 1 (as int)(num of HIMYM in series)#
# series.write_back([list, of, changed, results(documents)])
#
#
# dict for db
# {
#     'stats:{
#          '1': {'series_num' : 2}
#     },
#     'series' : [
#         "1": {
#             'name':'One Punch Man',
#             'curr_season' : 2,
#             'curr_episode' : 11,
#             'next_episode' : Null,
#             'failed_download_attempts' : 0,
#             'num_of_available' : 11,
#             'release_day' : 'mon',
#             'available_episodes' :
#             # format:
#             # {
#             #   "season num" : [list,of,episodes],
#             #   "season num" : [list,of,episodes]
#             # }
#             {
#                 "1" : [1, 2, 3, 4, 5, 6],
#                 "2" : [1, 2, 3, 4, 5]
#             }
#         },
#         "2" : {
#             'name':'Final Space',
#             'curr_season': 2,
#             'curr_episode': 4,
#             'next_episode': 5,
#             'failed_download_attempts': 1
#             'num_of_available' : 4,
#             'release_day' : 'mon',
#             'available_episodes' :
#             {
#                 "2" : [1, 2, 3, 4]
#             }
#
#         {
#     ]
# }


# -----------------------------------------------------Arguments----------------------------------------------------- #


def resolve_args():
    # get and parse arguments
    parser = argparse.ArgumentParser(
        prog='automan',
        description='Auto Torrent Manager',
        epilog='Created by Daniel Lisachuk as a leisure project / coding challenge'
    )

    # Non Command Flags
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

    # The RM Command
    RM_parser = subpursers.add_parser('remove', help='Remove Series From Monitoring')
    RM_group = RM_parser.add_mutually_exclusive_group(required=True)
    RM_group.add_argument('-s',
                          dest='Series',
                          help='Name of the Series to be Removed')
    RM_group.add_argument('-all', dest='purge',
                          action='store_true',
                          help='Purge DB of all monitored Series')

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


# ------------------------------------------------------Database------------------------------------------------------ #


def add_to_db(series_name, relese_day):
    db = TinyDB('./db.json')

    series = db.table('series')
    q_series = Query()

    if debugging:
        print('adding "{}" which is released every {} to DB'.format(series_name, relese_day))
        print('num of series before insertion is {}'.format(len(series)))

    if series.get(q_series.name == series_name) is None:

        new_series = {'name': series_name.lower(),
                      'curr_season': 1,
                      'curr_episode': 0,
                      'next_episode': 1,
                      'num_of_available': 0,
                      'release_day': relese_day,
                      'available_episodes': {"1": []}}

        series.insert(new_series)

        if debugging:
            print('num of series after insertion is {}'.format(len(series)))

    else:
        print('{} already exists in DB'.format(series_name))

    db.close()


def remove_from_db(series_name, purge):
    db = TinyDB('./db.json')

    series = db.table('series')
    q_series = Query()

    if debugging:
        print('num of series before removal is {}'.format(len(series)))
        print('removing "{}" from DB'.format(series_name))

    if purge:
        series.purge()

    # if removing specific series
    # if removal was successful
    elif len(series.remove(q_series.name == series_name)) is not 0:
        if debugging:
            print('{} was removed from DB'.format(series_name))

        if debugging:
            print('num of series after removal is {}'.format(len(series)))

    else:
        print("{} doesn't exist in DB".format(series_name))

    db.close()


# ------------------------------------------------------CronTab------------------------------------------------------ #


def add_to_crontab(series, release_day=None):
    if not release_day:
        release_day = 'mon'

    if debugging:
        print("adding {} to cron on {}".format(series, release_day))

    cron = CronTab(user=True)

    for job in cron:
        if '"{}"'.format(series) in job.command:
            print('[!] Series {} Already Exists'.format(series))
            return

    command = 'automan get "{}"'.format(series)
    comment = 'AuToMan - {} New Episode on {}'.format(series, release_day)

    if debugging:
        print('Scheduling New Cron Job\nCommand is {}\nComment is {}'.format(command, comment))

    new_job = cron.new(command=command, comment=comment)
    new_job.minute.on(30)
    new_job.hour.on(21)
    new_job.dow.on(release_day.upper())

    if debugging:
        print('new job is : {}'.format(str(new_job)))

    add_to_db(series, release_day)

    print('[+] Series "{}" Was Successfully Added To Monitoring'.format(series))
    cron.write()


def remove_from_crontab(series, purge):

    cron = CronTab(user=True)

    if purge:
        print('[+] Purging Cron of all Monitored Series')
        cron.remove_all(command='automan')
        remove_from_db(series, purge)
        done = True

    else:
        for job in cron:
            if '"{}"'.format(series) in job.command:
                if debugging:
                    print('Removing Series "{} From Cron"'.format(series))
                cron.remove(job)

                remove_from_db(series, purge)

                done = True

                print('[+] Series "{}" Has Been Successfully Removed From Monitoring'.format(series))

    if done:
        cron.write()
    else:
        print('[+] Series "{}" Is Not Monitored via Cron'.format(series))


# * open selenium(firefox)/ beautiful soup(browser-less)
#     -go to rarbg with args (will be provided by cron)
#         # format is 'https://rarbgtor.org/torrents.php?search=final+space+s02+e03&category%5B%5D=41'
#         # category = 'TV HD Episodes'
#
#     /or/
#
#     -go to pirate bay proxy
#         -go to first proxy option with args (will be provided by cron or manually)
#             # episode format is 'https://pirateproxy.ch/search/final space s01e01 1080p/0/99/200'
#             # season format is 'https://pirateproxy.ch/search/final space season 1 1080p/0/99/200'
# * form a request using chosen format
# * Find out if there are any results
#     -if no results
#         - display appropriate massage asking to try manual download
#     -else
#         - find first result + 'click' it
#             - find magnet link/torrent hash/torrent link/(whatever transmissionrpc needs)[find out]
#             ? implement & call new func 'download()' ?
#             - paste it into add_torrent()
#             - configure torrent
#                 # destination folder
#                 # etc...
#             - start it (in thread?)


# -----------------------------------------------------Downloads----------------------------------------------------- #


def download_next_episode():
    if debugging:
        print("downloading next episode")


def download_season(Sreies, season):
    if debugging:
        print("downloading whole season")


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


# --------------------------------------------------------List-------------------------------------------------------- #


def list_monitored_series(ll):
    db = TinyDB('./db.json')

    series = db.table('series')

    all_series = series.all()

    # long listing
    if ll:
        table = [['Name', 'Release Day', 'Current Season', 'Current Episode', 'Next Episode']]
        for serie in all_series:
            serie_cred = [serie['name'].capitalize(), serie['release_day'].capitalize(),
                          serie['curr_season'], serie['curr_episode'], serie['next_episode']]
            table.append(serie_cred)

        print(tabulate(table, headers='firstrow', tablefmt='grid',
                       colalign=('center', 'center', 'center', 'center', 'center')))


    # regular
    else:
        names = []
        for serie in all_series:
            names.append(serie['name'].capitalize())

        print(tabulate({'Name': names}, headers='keys', tablefmt='grid', colalign=('center',)))


# --------------------------------------------------------Main-------------------------------------------------------- #


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
        add_to_crontab(args.Series.lower(), args.day)

    # if removing from db
    elif 'purge' in args.__dict__:
        if args.Series is not None:
            remove_from_crontab(args.Series.lower(), args.purge)
        else:
            remove_from_crontab(None, args.purge)

    # if downloading an episode
    elif 'season' in args.__dict__:
        # if manual input #
        # - if all data is ok -- download specific episode
        if args.episode is not None and args.season is not None:
            download_specific_episode(args.Series.lower(), args.season, args.episode)

        # - if missing episode -- download whole season
        if args.episode is None and args.season is not None:
            download_season(args.Sreies.lower(), args.season)

        # - if missing season
        if args.episode is not None and args.season is None:
            print('Manual Mode Error: Missing Season No.')

        #  - if auto download
        if args.episode is None and args.season is None:
            download_next_episode(args.Series.lower())  # auto download next episode in line TODO SERIES-SEASON-EPISODE DATABASE

    # if listing all series
    elif 'long_listing' in args.__dict__:
        list_monitored_series(args.long_listing)

    print('Exiting...')
    print('Good Bye...')


if __name__ == '__main__':
    main()

