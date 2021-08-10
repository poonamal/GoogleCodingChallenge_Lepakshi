"""A video player class."""

import random
from video_library import VideoLibrary
import video_command
from video_playback import VideoPlayback, PlaybackState

def _print_video_choice_list(videos):
    for i, video in enumerate(videos, start=1):
        print(f"  {i}) {video})")

    print("Would you like to play any of the above? If yes, specify the number of the video.")
    print("If your answer is not a valid number, we will assume it's a no.")

    user_input = input("")

    try:
        num = int(user_input)
    except ValueError:
        num = 0

    if 1 <= num <= len(videos):
        return videos[num - 1]
    else:
        return None


class VideoPlayer:
    def __init__(self):
        self._videos = VideoLibrary()
        self._playlists = video_command.PlaylistLibrary()
        self._playback = VideoPlayback()


    def number_of_videos(self):
        num_videos = len(self._videos.get_all_videos())
        print(num_videos, "videos in the library")


    def show_all_videos(self):
        print("Here's a list of all available videos:")
        for v in self._videos.get_all_videos():
            print(v)

    def play_video(self, video_id):
        video = self._videos[video_id]
        video.check_allowed()
        #return

        if self._playback.state != PlaybackState.STOPPED:
            self.stop_video()
        self._playback.play(video)
        print("Playing video:", video.title)

    def stop_video(self):
        video = self._playback.get_video()
        print("Stopping video:", video.title)
        self._playback.stop()

    def play_random_video(self):
        random_video_id = self._videos.get_random_video_id()

        if random_video_id is None:
            print("No videos available")
        else:
            self.play_video(random_video_id)

    def pause_video(self):
        video = self._playback.get_video()
        if self._playback.state == PlaybackState.PAUSED:
            print("Video already paused:", video.title)
            return

        print("Pausing video:", video.title)
        self._playback.pause()

    def continue_video(self):
        video = self._playback.get_video()
        self._playback.resume()
        print("Continuing video:", video.title)
        
    #to be tested
    def show_playing(self):
        if self._playback.state == PlaybackState.PLAYING:
            print("Currently playing the video:", self._playback.get_video())
        elif self._playback.state == PlaybackState.PAUSED:
            print("Currently paused:", self._playback.get_video() - PAUSED)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        self._playlists.create(playlist_name)
        print("Successfully created new playlist:", playlist_name)            

    def add_to_playlist(self, playlist_name, video_id):
        playlist = self._playlists[playlist_name]
        video = self._videos[video_id]
        print(video)
        video.check_allowed()
        playlist.add_video(video)
        print("Added video to", playlist_name, video.title)

    def show_all_playlists(self):
        playlists = list(self._playlists.get_all())
        if not playlists:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        for playlist in playlists:
            print(playlist)

    def show_playlist(self, playlist_name):
        playlist = self._playlists[playlist_name]

        print("Showing playlist:", playlist_name)

        if not playlist.videos:
            print("No videos here yet")
            return

        for video in playlist.videos:
            print(f"  {video}")

    def remove_from_playlist(self, playlist_name, video_id):
        
        playlist = self._playlists[playlist_name]
        video = self._videos[video_id]
        playlist.remove_video(video)
        print("Removed video from", playlist_name,":", video.title)

    def clear_playlist(self, playlist_name):       
        playlist = self._playlists[playlist_name]
        playlist.clear()
        print("Successfully removed all videos from", playlist_name)
    
    def delete_playlist(self, playlist_name):      
        if playlist_name == None:
            print("playlist name not found")
        playlist = self._playlists[playlist_name]
        del self._playlists[playlist_name]
        print("Deleted playlist:", playlist_name)

    def search_videos(self, search_term):        
        results = self._videos.search_videos(search_term)

        if not results:
            print("No search results for", search_term)
            return

        print("Here are the results for", search_term)
        chosen_video = _print_video_choice_list(results)

        if chosen_video is not None:
            self.play_video(chosen_video.video_id)

    def search_videos_tag(self, video_tag):
        results = self._videos.get_videos_with_tag(video_tag)

        if not results:
            print("No search results for", video_tag)
            return

            print("Here are the results for", video_tag)
        chosen_video = _print_video_choice_list(results)

        if chosen_video is not None:
            self.play_video(chosen_video.video_id)

    def flag_video(self, video_id, flag_reason=""):
        if not flag_reason:
            flag_reason = "Not supplied"

        video = self._videos[video_id]

        if self._playback.state != PlaybackState.STOPPED and self._playback.get_video() == video:
            self.stop_video()

        video.flag(flag_reason)
        print("Successfully flagged video:",video.title, video.formatted_flag_reason)

    def allow_video(self, video_id):
        video = self._videos[video_id]
        video.unflag()
        print("Successfully removed flag from video:", video.title)
     