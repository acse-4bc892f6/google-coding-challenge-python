"""A video player class."""
import sys 
sys.path.append('./')

from video_library import VideoLibrary

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playing_title = None
        self._playing_id = None
        self._pausing_title = None
        self._pausing_id = None
        self._playlist_name_input = []
        self._playlist_name_upper = []
        self._playlist_videos = {}
        self._flagged_video = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_info = {}
        for i in self._video_library.get_all_videos():
            tag = []
            for j in i.tags:
                tag.append(j)
            tag = ' '.join(tag)
            all_info[i.title] = [i.video_id, tag]
        info = all_info.items()
        sorted_info = sorted(info)
        print(f"Here's a list of all available videos:")
        for i in range(len(sorted_info)):
            if sorted_info[i][1][0] not in self._flagged_video.keys():
                print(f"{sorted_info[i][0]} ({sorted_info[i][1][0]}) [{sorted_info[i][1][1]}]") 
            else:
                print(f"{sorted_info[i][0]} ({sorted_info[i][1][0]}) [{sorted_info[i][1][1]}] - FLAGGED (reason: {self._flagged_video[sorted_info[i][1][0]]})")
    
    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video_object = self._video_library.get_video(video_id)
        if video_object == None:
            print(f"Cannot play video: Video does not exist")
        else:
            play_title = video_object.title
            play_id = video_object.video_id
            if self._playing_title == None:
                if play_id not in self._flagged_video:
                    print(f"Playing video: {play_title}")
                    self._playing_title = play_title
                    self._playing_id = play_id
                    if self._pausing_title != None:
                        self._pausing_title = None
                        self._pausing_id = None
                else:
                    print(f"Cannot play video: Video is currently flagged (reason: {self._flagged_video[play_id]})")
            else:
                if play_id not in self._flagged_video:
                    print(f"Stopping video: {self._playing_title}")
                    print(f"Playing video: {play_title}")
                    self._playing_title = play_title
                    self._playing_id = play_id
                else:
                    print(f"Cannot play video: Video is currently flagged (reason: {self._flagged_video[play_id]})")

    def stop_video(self):
        """Stops the current video."""

        if self._playing_title != None and self._pausing_title == None:
            print(f"Stopping video: {self._playing_title}")
            self._playing_title = None
            self._playing_id = None
        elif self._pausing_title != None and self._playing_title == None:
            print(f"Stopping video: {self._pausing_title}")
            self._pausing_title = None
            self._pausing_id = None
        elif self._playing_title == None and self._pausing_title == None:
            print(f"Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        import random
        all_videos = self._video_library.get_all_videos()
        valid_id = []
        for i in range(len(all_videos)):
            valid_id.append(all_videos[i].video_id)
        for key in self._flagged_video:
            if key in valid_id:
                valid_id.remove(key)
            else:
                continue
        if len(valid_id) == 0:
            print(f"No videos available")
        else:
            index = random.randint(0, len(valid_id))
            random_video = self._video_library.get_video(valid_id[index])
            random_title = random_video.title
            random_id = all_videos[index].video_id
            if self._playing_title == None:
                print(f"Playing video: {random_title}")
                self._playing_title = random_title
                self._playing_id = random_id
            else:
                print(f"Stopping video: {self._playing_title}")
                print(f"Playing video: {random_title}")
                self._playing_title = random_title
                self._playing_id = random_id

    def pause_video(self):
        """Pauses the current video."""

        if self._playing_title == None and self._pausing_title == None:
            print(f"Cannot pause video: No video is currently playing")
        elif self._playing_title != None and self._pausing_title == None:
            print(f"Pausing video: {self._playing_title}")
            self._pausing_title = self._playing_title
            self._pausing_id = self._playing_id
            self._playing_title = None
            self._playing_id = None
        elif self._playing_title == None and self._pausing_title != None:
            print(f"Video already paused: {self._pausing_title}")

    def continue_video(self):
        """Resumes playing the current video."""

        if self._pausing_title == None and self._playing_title != None:
            print(f"Cannot continue video: Video is not paused")
        elif self._pausing_title == None and self._playing_title == None:
            print(f"Cannot continue video: No video is currently playing")
        else:
            print(f"Continuing video: {self._pausing_title}")
            self._playing_title = self._pausing_title
            self._pausing_title = None
            self._playing_id = self._pausing_id
            self._pausing_id = None

    def show_playing(self):
        """Displays video currently playing."""

        if self._playing_id != None and self._pausing_id == None:
            video_object = self._video_library.get_video(self._playing_id)
            tag = []
            for i in video_object.tags:
                tag.append(i)
            tag = ' '.join(tag)
            print(f"Currently playing: {video_object.title} ({video_object.video_id}) [{tag}]")
        elif self._pausing_id != None and self._playing_id == None:
            video_object = self._video_library.get_video(self._pausing_id)
            tag = []
            for i in video_object.tags:
                tag.append(i)
            tag = ' '.join(tag)
            print(f"Currently playing: {video_object.title} ({video_object.video_id}) [{tag}] - PAUSED")
        elif self._playing_id == None and self._pausing_id == None:
            print(f"No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.upper() not in self._playlist_name_upper:
            print(f"Successfully created new playlist: {playlist_name}")
            self._playlist_name_input.append(playlist_name)
            self._playlist_name_upper.append(playlist_name.upper())
            self._playlist_videos[playlist_name.upper()] = []
        else:
            print(f"Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        
        video_object = self._video_library.get_video(video_id)
        if video_id in self._flagged_video:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {self._flagged_video[video_id]})")
        else: 
            if playlist_name.upper() not in self._playlist_name_upper:
                print(f"Cannot add video to another_playlist: Playlist does not exist")
            else:
                #video_object = self._video_library.get_video(video_id)
                if video_object == None:
                    print(f"Cannot add video to {playlist_name}: Video does not exist")
                else:
                    video_title = video_object.title
                    if video_id not in self._playlist_videos[playlist_name.upper()]:
                        self._playlist_videos[playlist_name.upper()].append(video_id)
                        print(f"Added video to {playlist_name}: {video_title}")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")


    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlist_name_input) == 0:
            print(f"No playlists exist yet")
        else:
            playlist_name_sorted = self._playlist_name_input.sort()   
            print(f"Showing all playlists:")
            for i in self._playlist_name_input:
                print(i)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        if playlist_name.upper() not in self._playlist_name_upper:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            if len(self._playlist_videos[playlist_name.upper()]) == 0:
                print(f"Showing playlist: {playlist_name}")
                print(f"No videos here yet")
            else:
                print(f"Showing playlist: {playlist_name}")
                for id in self._playlist_videos[playlist_name.upper()]:
                    video_object = self._video_library.get_video(id)
                    tag = []
                    for i in video_object.tags:
                        tag.append(i)
                    tag = ' '.join(tag)
                    if id not in self._flagged_video.keys():
                        print(f"{video_object.title} ({id}) [{tag}]")
                    else:
                        print(f"{video_object.title} ({id}) [{tag}] - FLAGGED (reason: {self._flagged_video[id]})")
                    


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() not in self._playlist_name_upper:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            if video_id not in self._playlist_videos[playlist_name.upper()]:
                if self._video_library.get_video(video_id) == None:
                    print(f"Cannot remove video from {playlist_name}: Video does not exist")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                self._playlist_videos[playlist_name.upper()].remove(video_id)
                video_object = self._video_library.get_video(video_id)
                print(f"Removed video from {playlist_name}: {video_object.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlist_name_upper:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            self._playlist_videos[playlist_name.upper()].clear()
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() not in self._playlist_name_upper:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            del self._playlist_videos[playlist_name.upper()]
            self._playlist_name_upper.remove(playlist_name.upper())
            for element in self._playlist_name_input:
                element_upper = element.upper()
                if element_upper == playlist_name.upper():
                    self._playlist_name_input.remove(element)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        search_term_upper = search_term.upper()
        all_info = {}
        for i in self._video_library.get_all_videos():
            tag = []
            for j in i.tags:
                tag.append(j)
            tag = ' '.join(tag)
            all_info[i.title] = [i.video_id, tag]
        valid_keys = []
        for key in all_info:
            key_upper = key.upper()
            if search_term_upper in key_upper: 
                valid_keys.append(key)
            else:
                continue
        valid_keys.sort()
        for k in valid_keys:
            if all_info[k][0] in self._flagged_video.keys():
                valid_keys.remove(k)
            else:
                continue
        if len(valid_keys) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i in range(len(valid_keys)):
                print(f"{i+1}) {valid_keys[i]} ({all_info[valid_keys[i]][0]}) [{all_info[valid_keys[i]][1]}]")
            print(f"Would you like to play any of the above? If yes, specify the number of the video.\n"
            "If your answer is not a valid number, we will assume it's a no.")
            response = input()
            ints = [i for i in range(1, len(valid_keys)+1)]
            string_ints = [str(int) for int in ints]
            if response in string_ints:
                index = int(response)
                self.play_video(all_info[valid_keys[index-1]][0])
            else:
                return 0

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        video_tag_upper = video_tag.upper()
        all_info = {}
        for i in self._video_library.get_all_videos():
            tag = []
            for j in i.tags:
                tag.append(j)
            tag = ' '.join(tag)
            all_info[i.title] = [i.video_id, tag]
        valid_tags = []
        all_tags = []
        for key in all_info:
            all_tags.append(all_info[key][1])
        for tag in all_tags:
            tag_words = tag.split()
            tag_words_upper = [word.upper() for word in tag_words]
            if video_tag_upper in tag_words_upper:
                valid_tags.append(tag)
            else:
                continue
        valid_keys = []
        for key in all_info:
            if all_info[key][1] in valid_tags:
                valid_keys.append(key)
            else:
                continue
        valid_keys.sort()
        for k in valid_keys:
            if all_info[k][0] in self._flagged_video.keys():
                valid_keys.remove(k)
            else:
                continue
        if len(valid_tags) == 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(valid_keys)):
                print(f"{i+1}) {valid_keys[i]} ({all_info[valid_keys[i]][0]}) [{all_info[valid_keys[i]][1]}]")
            print(f"Would you like to play any of the above? If yes, specify the number of the video.\n"
            "If your answer is not a valid number, we will assume it's a no.")
            response = input()
            ints = [i for i in range(1, len(valid_keys)+1)]
            string_ints = [str(int) for int in ints]
            if response in string_ints:
                index = int(response)
                self.play_video(all_info[valid_keys[index-1]][0])
            else:
                return 0   

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_object = self._video_library.get_video(video_id)
        if video_object == None:
            print(f"Cannot flag video: Video does not exist")
        else:
            video_title = video_object.title
            if video_id in self._flagged_video:
                print(f"Cannot flag video: Video is already flagged")
            else:
                if len(flag_reason) == 0:
                    flag_reason_fill = "Not supplied"
                    self._flagged_video[video_id] = flag_reason_fill
                else:
                    self._flagged_video[video_id] = flag_reason
                if (self._playing_id != None and self._playing_id == video_id) or (self._pausing_id != None and self._pausing_id == video_id):
                    self.stop_video()
                print(f"Successfully flagged video: {video_title} (reason: {self._flagged_video[video_id]})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_object = self._video_library.get_video(video_id)
        if video_object == None:
            print(f"Cannot remove flag from video: Video does not exist")
        else:
            video_title = video_object.title
            if video_id not in self._flagged_video:
                print(f"Cannot remove flag from video: Video is not flagged")
            else:
                del self._flagged_video[video_id]
                print(f"Successfully removed flag from video: Amazing Cats")
            
