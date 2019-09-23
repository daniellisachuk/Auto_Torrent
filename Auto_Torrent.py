#!/usr/bin/env python

# requires transmission web client to be active
# (transmission-gtk -> edit -> preferences -> remote(tab) -> allow remote access(enable))

import subprocess
import logging
import argparse
import requests
import transmissionrpc as transmission
from tinydb import TinyDB, Query
from crontab import CronTab
from tabulate import tabulate
from bs4 import BeautifulSoup


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

    # the CATCH-UP Command
    CU_parser = subpursers.add_parser('catch-up', help='Download the Current Running Season up to Latest Episode')
    CU_parser.add_argument('-s',
                           dest='cu_series',
                           required=True,
                           help='Name of the Series to be Caught Up (has to be added first)')

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
                      'available_episodes': {"1": []},
                      'target_dir': '~/Series/{}/'.format(series_name.lower())}

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


# ------------------------------------------------------Scraping------------------------------------------------------ #





def search_series_info():
    pass


def search_in_pirate_bay():
    pass


def search_in_rarbg(series_name, season, episode):
    # initial errors

    if not series_name:
        print('[!] Something Went Horribly Wrong While Entering The Torrent Name')
        return

    # episode but not season error
    if series_name and episode and not season:
        return

    response = requests.get('https://rarbgtor.org/torrents.php?search=final+space+s02+e03&category%5B%5D=41')
    parser = BeautifulSoup(response.text, 'html.parser')
    search_results = parser.find_all('div', class_='a')


# maybe:
# def search_in_kat():
#     pass

# -----------------------------------------------------Downloads----------------------------------------------------- #



def download_next_episode():
    if debugging:
        print("downloading next episode")


def download_season(Sreies, season):
    if debugging:
        print("downloading whole season")


def download_specific_episode(series, season, episode):
    pass


def catch_up():
    pass


# --------------------------------------------------------List-------------------------------------------------------- #


def list_monitored_series(ll):
    db = TinyDB('./db.json')

    series = db.table('series')

    all_series = series.all()

    if len(all_series) is not 0:
        # long listing
        if ll:
            table = [['Name', 'Release Day', 'Current Season', 'Current Episode', 'Next Episode',
                      'No. Available Episodes', 'Series Directory']]
            for serie in all_series:
                serie_cred = [serie['name'].capitalize(), serie['release_day'].capitalize(),
                              serie['curr_season'], serie['curr_episode'], serie['next_episode'],
                              serie['num_of_available'], serie['target_dir']]
                table.append(serie_cred)

            print(tabulate(table, headers='firstrow', tablefmt='grid',
                           colalign=('center', 'center', 'center', 'center', 'center', 'center')))
        # regular
        else:
            table = []
            for serie in all_series:
                serie_cred = [serie['name'], serie['num_of_available']]
                table.append(serie_cred)

            print(tabulate(table, headers=['Name', 'No. Available Episodes'],
                           tablefmt='grid', colalign=('center', 'center')))
    else:
        print('[!] No Series Currently Being Monitored')


# --------------------------------------------------------Main-------------------------------------------------------- #
# TODO ~!!~CLEAN(/FILTER) USER INPUT~!!~

def main():
    global debugging

    args = resolve_args()
    args_dict = args.__dict__

    # TODO implement logger with basic level
    debugging = True  # TODO WHEN FINISHED CHANGE BACK TO : args.debug
    # debug massage
    if debugging:
        print(args_dict)
        # TODO set implemented logger to DEBUG level
    # if adding a new series
    if 'day' in args_dict:
        add_to_crontab(args.Series.lower(), args.day)

    # if removing from db
    elif 'purge' in args_dict:
        if args.Series is not None:
            remove_from_crontab(args.Series.lower(), args.purge)
        else:
            remove_from_crontab(None, args.purge)

    # if catching up
    elif 'cu_series' in args_dict:
        print('catching up')

    # if downloading an episode
    elif 'season' in args_dict:
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
            download_next_episode(args.Series.lower())  # auto download next episode in line

    # if listing all series
    elif 'long_listing' in args_dict:
        list_monitored_series(args.long_listing)

    print('Exiting...')
    print('Good Bye...')


if __name__ == '__main__':
    main()

