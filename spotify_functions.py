import spotipy
import discord


spotify = None


def instantiate_spotify(authorization):
    """Instantiates spotipy"""
    global spotify
    spotify = spotipy.Spotify(auth=authorization)


def existing_playlist(user_id, community_playlist_name):
    """Checks for an existing playlist with community_playlist_name in a user's playlists"""
    for playlist in spotify.user_playlists(user_id)['items']:
        if playlist['name'] == community_playlist_name:
            print("Playlist already exists")
            return True


def create_playlist(user_id, community_playlist_name):
    """Creates a playlist with community_playlist_name for a user"""
    spotify.user_playlist_create(user_id, community_playlist_name)
    print("Playlist created")


def get_playlist_id(user_id, community_playlist_name):
    """Gets the playlist id of a playlist with community_playlist_name for a user"""
    for playlist in spotify.user_playlists(user_id)['items']:
        if playlist['name'] == community_playlist_name:
            return playlist['uri'][17:]  # Add else


def get_track_id(artist_song):
    """Searches Spotify for a song and returns the track id"""
    if spotify.search(artist_song, 1)['tracks']['items']:
        track_id = spotify.search(artist_song, 1)['tracks']['items'][0]['uri'][14:]
        print("Found track id")
        return track_id
    print("Could not find track\n")


def existing_track(playlist_id, track_id):
    """Checks for an existing track id in a playlist"""
    for track in spotify.playlist_tracks(playlist_id)['items']:
        if track['track']['uri'][14:] == track_id:
            print("Track already in playlist\n")
            return True


def add_track(user_id, playlist_id, track_id):
    """Adds a track to a playlist"""
    spotify.user_playlist_add_tracks(user_id, playlist_id, [track_id])
    print("Track added\n")


def community_playlist(auth, community_playlist_name, artist_song):
    """Manages community playlist creation and track addition"""
    instantiate_spotify(auth)
    user_id = spotify.me()['id']
    track_id = get_track_id(artist_song)
    if track_id:
        if not existing_playlist(user_id, community_playlist_name):
            create_playlist(user_id, community_playlist_name)
        playlist_id = get_playlist_id(user_id, community_playlist_name)
        if not existing_track(playlist_id, track_id):
            add_track(user_id, playlist_id, track_id)


def existing_spotipy_instance():
    if spotify == None:
        return False
    return True


def get_playlist_url(user_id, community_playlist_name):
    """Get a playlist url given a user_id and the community_playlist_name"""
    for playlist in spotify.user_playlists(user_id)['items']:
        if playlist['name'] == community_playlist_name:
            return playlist['external_urls']['spotify']


def rename_playlist(user_id, community_playlist_name, new_community_playlist_name):
    """Rename a playlist on Spotify"""
    playlist_id = get_playlist_id(user_id, community_playlist_name)
    if playlist_id:
        spotify.user_playlist_change_details(user_id, playlist_id, name=new_community_playlist_name)
    else:
        print("Could not find playlist id")






