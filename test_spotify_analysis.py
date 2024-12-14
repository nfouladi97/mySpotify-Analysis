""" Test the functions and methods of Spotify Analysis """

# Import modules
import spotify_analysis
import unittest
import os
from unittest import mock


def test_get_spotify_data():
    """Tests get_spotify_data method."""

    # Assert dataframe
    assert not spotify_analysis.get_spotify_data().empty


class SpotifyAnalysisTests(unittest.TestCase):
    """A class to test spotify_analysis.py methods"""

    def setUp(self):
        """Sets up the tests"""

        self.plot = spotify_analysis.Plot("data/test.csv")

    def tearDown(self):
        """Tears down the tests"""

        self.plot = None

    @mock.patch("%s.spotify_analysis.plt" % __name__)
    def test_bar_plot_top_10_frequency(self, mock_plt):
        """Tests bar_plot_top_10_frequency method."""

        # Call bar_plot_top_10_frequency method
        self.plot.bar_plot_top_10_frequency()

        # Assert plt.show got called.
        assert mock_plt.show.called

    @mock.patch("%s.spotify_analysis.plt" % __name__)
    def test_pie_plot_top_10_frequency(self, mock_plt):
        """Tests pie_plot_top_10_frequency method"""

        # Call pie_plot_top_10_frequency method
        self.plot.pie_plot_top_10_frequency()

        # Assert plt.show got called
        assert mock_plt.show.called

    def test_save_to_csv_file(self):
        """Tests save_to_csv_file method."""

        # Save dataframe with new name.
        self.plot.save_to_csv_file("unit_test")

        # Assert file exists.
        assert os.path.isfile("unit_test.csv")


if __name__ == "__main__":
    unittest.main()
