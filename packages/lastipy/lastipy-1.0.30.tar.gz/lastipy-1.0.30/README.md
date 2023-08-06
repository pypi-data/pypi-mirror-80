
<h1>Lastipy</h1>
<b>Lastipy</b> is a Python library combining the APIs of Spotify and Last.fm, with scripts for things like creating customized recommendation playlists, automatically saving new releases, etc. 
<h2>Prerequisites</h2>
You will need API keys for Last.fm: https://www.last.fm/api/ and for Spotify: https://developer.spotify.com/documentation/web-api/<br/>.
<h2>Installation</h2>
Clone the project, navigate to the project directory then use pip to install (will automatically pick up setup.py):

```
pip install .
```
<h2>Usage</h2>
The first time any of the scripts are run, the Spotify user will need to give authorization to the application in order to be able to read/modify their playlists/library. Once prompted, open the given URL in a browser, log into Spotify, then copy the URL to which you are redirected and paste it into the console. This will only need to be done the first time, since spotipy will cache the authorization.  
<h3>Creating a recommendations playlist</h3>
To create a playlist of recommendations generated from the user's "top tracks" in Last.fm, run:

```
recommendations_playlist user-configuration-file api-keys-file 
```
See scripts/example.recommendations.config for an example user configuration file and scripts/example.keys for an example API keys file.<br/>
<h3>Save new releases from followed artists to library</h3>
To save new tracks released by the user's followed artists (as of the current date) to their library ("Liked Songs"), run: 

```
save_new_tracks spotify_user api_keys_file --ignore-remixes
```
<b>Note</b> that the --ignore-remixes flag is optional.
<br />
See scripts/example.keys for an an example API keys file.
