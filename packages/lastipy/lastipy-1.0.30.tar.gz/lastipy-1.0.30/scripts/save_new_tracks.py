#!/usr/bin/env python3.7

from configparser import ConfigParser
import argparse
import os
from lastipy import definitions
from lastipy.lastfm.library.top_tracks import fetch_top_tracks
from lastipy.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from lastipy.lastfm.recommendations.recommendations import fetch_recommendations
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks
from lastipy.lastfm.library.recent_artists import fetch_recent_artists
from lastipy.lastfm.library import period
from lastipy.spotify import playlist, search, library
from lastipy.track import Track
from numpy.random import choice
from spotipy import Spotify
from lastipy.spotify import token
from lastipy.util.setup_logging import setup_logging
import logging
from lastipy.spotify import new_releases
from datetime import datetime
from lastipy.util.parse_api_keys import ApiKeysParser


def save_new_tracks():
    """Saves new tracks (as of the current date) from the specified Spotify user's followed artists to their library"""

    setup_logging("new_releases.log")
    args = _extract_args()
    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    new_tracks = new_releases.fetch_new_tracks(spotify, args.ignore_remixes)

    if len(new_tracks) > 0:
        # Only process further if we actually fetched any new tracks
        library.add_tracks_to_library(spotify, new_tracks)
    else:
        logging.info("No new tracks to add!")

    logging.info("Done!")

def _extract_args():
    args = _parse_args()

    # Parse API keys file
    keys_parser = ApiKeysParser(args.api_keys_file)
    args.spotify_client_id_key = keys_parser.spotify_client_id_key
    args.spotify_client_secret_key = keys_parser.spotify_client_secret_key
    
    return args

def _parse_args():
    args_parser = argparse.ArgumentParser(description="Adds new tracks from the given user's followed artists to their saved/liked tracks")
    args_parser.add_argument('spotify_user', type=str)
    args_parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    args_parser.add_argument('--ignore-remixes', dest='ignore_remixes', action='store_true', default=False)
    return args_parser.parse_args()

if __name__ == "__main__":
    save_new_tracks()