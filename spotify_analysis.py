"""A python script that will analyze a dataset from Spotify’s Billboard Hot 100 2019.
Author: Nour Fouladi

"""

# Import modules.
import argparse
import sys
import matplotlib.pyplot as plt
import pandas
import spotipy
from matplotlib.ticker import MaxNLocator


def get_spotify_data():
    """Creates data frame from current Spotify's Billboard Hot 100.

    Returns:
        data frame obj: the Hot 100 songs.
    """

    # Get Spotify credentials.
    from spotipy.oauth2 import SpotifyClientCredentials

    # Enter Spotify API keys here.
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        # Enter client ID key here as a string.
        client_id="",
        # Enter client secret key here as a string.
        client_secret=""))

    sp.trace = False

    # Billboard Top 100 Playlist.
    playlist = sp.playlist("6UeSakyzhiEt4NB3UAd6NQ?si=1Rwmvg38SYy4Tg2RAaGEKQ")

    # SOURCE:
    # Author: Max Hilsdorf
    # Title: How to Create Large Music Datasets Using Spotipy
    # https://towardsdatascience.com/how-to-create-large-music-datasets-using-
    # spotipy-40e7242cc6a6

    # Create empty data frame.
    playlist_features_list = ["artist", "album", "track_name", "track_id",
                              "danceability", "energy", "key", "loudness",
                              "mode", "speechiness", "instrumentalness",
                              "liveness", "valence", "tempo", "duration_ms",
                              "time_signature"]

    # Create data frame columns.
    playlist_df = pandas.DataFrame(columns=playlist_features_list)

    # Loop through every track in the playlist, extract features and append the
    # features to the playlist data frame.
    for track in playlist["tracks"]["items"]:

        # Create dictionary and get metadata.
        playlist_features = {
            "artist": track["track"]["album"]["artists"][0]["name"],
            "album": track["track"]["album"]["name"],
            "track_name": track["track"]["name"],
            "track_id": track["track"]["id"]
        }

        # Get audio features.
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]

        # Concat the dfs.
        track_df = pandas.DataFrame(playlist_features, index=[0])
        playlist_df = pandas.concat([playlist_df, track_df], ignore_index=True)

    # Return data frame.
    return playlist_df


class Plot:
    """A class to analyze Spotify's Billboard Hot 100 songs.

    Attributes:
        data_frame (obj): the Hot 100 data frame.
    """

    def __init__(self, path=None):
        """Initializes a Plot object.

        Args:
            path (str): the path to the CSV file.
        """

        # If there is no path, call get_spotify_data() and get data frame,
        # else, read CSV file.
        if path is None:
            self.data_frame = get_spotify_data()
        else:
            self.data_frame = pandas.read_csv(path)

    def top_10_songs(self):
        """Prints top 10 songs.

        Side effects:
            Prints information to the console.
        """

        # Print top 10 songs.
        print(self.data_frame.head(10).track_name.to_string(index=False))

    def top_10_artists(self):
        """Prints top 10 artists.

        Side effects:
            Prints information to the console.
        """

        # Print top 10 artists.
        print(self.data_frame.head(10).artist.to_string(index=False))

    def bar_plot_top_10_frequency(self):
        """Plots top 10 artists frequency as bar plot.

        Side effects:
            Displays bar plot window.
        """

        # Get top 10 frequency.
        axes = self.data_frame["artist"].value_counts().nlargest(10).plot.bar(
            rot=0,
            color="turquoise",
            title="Top 10 Artists Frequency",
            legend=True
        )

        # Set labels.
        axes.set_xlabel("Artist", fontsize=12)
        axes.set_ylabel("Frequency", fontsize=12)
        axes.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Add values above bars.
        for p in axes.patches:
            axes.annotate("%.0f" % p.get_height(),
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha="center", va="center", xytext=(0, 10),
                          textcoords="offset points")

        # Show plot.
        plt.show()

    def pie_plot_top_10_frequency(self):
        """Plots top 10 artists frequency as pie chart.

        Side effects:
            Displays pie chart window.
        """

        # Get top 10 frequency.
        axes = self.data_frame["artist"].value_counts().nlargest(10).plot.pie(
            autopct="%1.1f%%",
            figsize=(10, 10),
            legend=True,
            title="Top 10 Artists Frequency"
        )

        # Set legend.
        axes.legend(
            loc="center left",
            bbox_to_anchor=(-0.1, 1)
        )

        # Show chart.
        plt.show()

    def box_plot_audio_metrics(self):
        """Plots top 10 artists frequency as box plot.

        Effects:
            Displays box plot window.
        """

        # Get danceability, energy, and speechiness audio metrics.
        axes = self.data_frame.boxplot(
            column=["danceability", "energy", "speechiness"],
            grid=False
        )

        # Set legend.
        axes.legend(
            labels=["danceability - how suitable a track is for dancing",
                    "energy - intensity and activity",
                    "speechiness - presence of spoken words"])

        # Set title.
        plt.title("Billboard Top 100 Danceability, Energy, & Speechiness")

        # Label axes.
        axes.set_xlabel("Audio Metric")
        axes.set_ylabel("Least to Most")

        # Display plot.
        plt.show()

    def save_to_csv_file(self, filename):
        """Saves data frame to CSV file.

        Args:
            filename (str): the filename.

        Effects:
            Creates CSV file.
        """

        # Save data frame to CSV file.
        self.data_frame.to_csv(f"{filename}.csv")


def main(path):
    """Creates an instance of the Plot class.

    Effects:
        Prints information to the console. Displays plot windows. Creates CSV
        file.
    """

    # Create an instance of the Plot.
    plot = Plot(path)

    # Loops while user chooses options.
    while True:
        # Show menu.
        print(57 * "-")
        print(f"MENU {path}")
        print(57 * "-")
        print("1. Top 10 Songs")
        print("2. Top 10 Artists")
        print("3. Bar Plot - Top 10 Artists Frequency")
        print("4. Pie Plot - Top 10 Artists Frequency")
        print("5. Box Plot - Top 100 Danceability, Energy, & Speechiness")
        print("6. Save to CSV file")
        print("7. Exit")
        print(57 * "-")
        print()

        # Prompt choice.
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            choice = None

        print()

        # Handle choice.
        # If choice is 1, call top_10_songs() method,
        # else if choice is 2, call top_10_artists() method,
        # else if choice is 3, call bar_plot_top_10_frequency() method,
        # else if choice is 4, call pie_plot_top_10_frequency() method,
        # else if choice is 5, call box_plot_audio_metrics() method,
        # else if choice is 6, call save_to_csv_file() method,
        # else if choice is 7, exit program,
        # else, print error.
        if choice == 1:
            plot.top_10_songs()
            print()
            input("Press ENTER to continue...")
            print()
        elif choice == 2:
            plot.top_10_artists()
            print()
            input("Press ENTER to continue...")
            print()
        elif choice == 3:
            plot.bar_plot_top_10_frequency()
        elif choice == 4:
            plot.pie_plot_top_10_frequency()
        elif choice == 5:
            plot.box_plot_audio_metrics()
        elif choice == 6:
            if path is None:
                # Prompt filename.
                filename = input("Enter filename: ")
                print()

                # Call save_to_csv_file() method.
                plot.save_to_csv_file(filename)

                # Print message to user.
                print("Saved to CSV file...")
                print()
            else:
                # Print error.
                print("Error. You are reading from a CSV file.")
                input("Press ENTER to continue...")
                print()
        elif choice == 7:
            # Print exit message.
            print("Exiting...")
            break
        else:
            # Print error.
            input("Error. Press ENTER to continue...")
            print()


def parse_args(my_args_list):
    """Parses the command line arguments for the program;
    this will result in a namespace object, which you should return.

    Args:
        my_args_list (str): a list of strings containing the command line
            arguments for the program.

    Returns:
        namespace object: the command line arguments namespace object.
    """

    # Create a new Parser instance.
    parser = argparse.ArgumentParser("Analyze a dataset from Spotify's "
                                     "Billboard Hot 100.")

    # Optional arguments.
    # The path to the text file.
    parser.add_argument("-p", "--path",
                        type=str,
                        help="the path to the csv file")

    # Parsing the list using the arguments defined in the parser object.
    # Use the parse_args() method of your ArgumentParser instance to parse the
    # list of strings that was passed to your function; this will result in a
    # namespace object, which you should return.
    args = parser.parse_args(my_args_list)

    # Return the namespace object.
    return args


if __name__ == '__main__':
    # Pass sys.argv[1:] to parse_args() and store the result in a
    # variable.
    args = parse_args(sys.argv[1:])

    # Call the main() function.
    main(args.path)
