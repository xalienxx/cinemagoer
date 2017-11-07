from pytest import fixture, mark

import re
from urllib.request import urlopen

from imdb.parser.http.movieParser import DOMHTMLMovieParser


@fixture(scope='module')
def movie_combined_details(movies):
    """A function to retrieve the combined details page of a test movie."""
    def retrieve(movie_key):
        url = movies[movie_key] + '/combined'
        return urlopen(url).read().decode('utf-8')
    return retrieve


parser = DOMHTMLMovieParser()


def test_cover_url_should_be_a_link(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['cover url'].endswith('.jpg')


def test_cover_url_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('aslan')
    data = parser.parse(page)['data']
    assert 'cover url' not in data


def test_title_should_not_have_year(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['title'] == 'The Matrix'


def test_title_tv_movie_should_not_include_type(movie_combined_details):
    page = movie_combined_details('matrix_tv')
    data = parser.parse(page)['data']
    assert data['title'] == 'The Matrix Defence'


def test_title_video_movie_should_not_include_type(movie_combined_details):
    page = movie_combined_details('matrix_video')
    data = parser.parse(page)['data']
    assert data['title'] == 'Armitage III: Poly Matrix'


def test_title_video_game_should_not_include_type(movie_combined_details):
    page = movie_combined_details('matrix_vg')
    data = parser.parse(page)['data']
    assert data['title'] == 'The Matrix Online'


def test_title_tv_series_should_not_have_quotes(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert data['title'] == 'Doctor Who'


def test_title_tv_mini_series_should_not_have_quotes(movie_combined_details):
    page = movie_combined_details('band_of_brothers')
    data = parser.parse(page)['data']
    assert data['title'] == 'Band of Brothers'


def test_title_tv_episode_should_not_be_series_title(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert data['title'] == 'Blink'


def test_year_should_be_an_integer(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['year'] == 1999


def test_year_followed_by_kind_in_full_title_should_be_ok(movie_combined_details):
    page = movie_combined_details('matrix_video')
    data = parser.parse(page)['data']
    assert data['year'] == 1996


def test_year_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('aslan')
    data = parser.parse(page)['data']
    assert 'year' not in data


def test_imdb_index_should_be_a_roman_number(movie_combined_details):
    page = movie_combined_details('mothers_day4')
    data = parser.parse(page)['data']
    assert data['imdbIndex'] == 'IV'


def test_imdb_index_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert 'imdbIndex' not in data


def test_kind_none_should_be_movie(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['kind'] == 'movie'


def test_kind_tv_movie_should_be_tv_movie(movie_combined_details):
    page = movie_combined_details('matrix_tv')
    data = parser.parse(page)['data']
    assert data['kind'] == 'tv movie'


def test_kind_video_movie_should_be_video_movie(movie_combined_details):
    page = movie_combined_details('matrix_video')
    data = parser.parse(page)['data']
    assert data['kind'] == 'video movie'


def test_kind_video_game_should_be_video_game(movie_combined_details):
    page = movie_combined_details('matrix_vg')
    data = parser.parse(page)['data']
    assert data['kind'] == 'video game'


def test_kind_tv_series_should_be_tv_series(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert data['kind'] == 'tv series'


def test_kind_tv_mini_series_should_be_tv_mini_series(movie_combined_details):
    page = movie_combined_details('band_of_brothers')
    data = parser.parse(page)['data']
    assert data['kind'] == 'tv mini series'


def test_kind_tv_series_episode_should_be_episode(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert data['kind'] == 'episode'


# def test_kind_short_movie_should_be_short_movie(movie_combined_details):
#     page = movie_combined_details('matrix_short')
#     data = parser.parse(page)['data']
#     assert data['kind'] == 'short movie'


# def test_kind_tv_short_movie_should_be_tv_short_movie(movie_combined_details):
#     page = movie_combined_details('matrix_tv_short')
#     data = parser.parse(page)['data']
#     assert data['kind'] == 'tv short movie'


# def test_kind_tv_special_should_be_tv_special(movie_combined_details):
#     page = movie_combined_details('roast_sheen')
#     data = parser.parse(page)['data']
#     assert data['kind'] == 'tv special'


@mark.fragile
def test_series_years_continuing_should_be_open_range(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert data['series years'] == '2005-'


def test_series_years_ended_should_be_closed_range(movie_combined_details):
    page = movie_combined_details('house')
    data = parser.parse(page)['data']
    assert data['series years'] == '2004-2012'


def test_series_years_mini_series_ended_in_same_year_should_be_closed_range(movie_combined_details):
    page = movie_combined_details('band_of_brothers')
    data = parser.parse(page)['data']
    assert data['series years'] == '2001-2001'


def test_series_years_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert 'series years' not in data


def test_number_of_episodes_should_be_an_integer(movie_combined_details):
    page = movie_combined_details('house_middle')
    data = parser.parse(page)['data']
    assert data['number of episodes'] == 176


def test_number_of_episodes_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('house')
    data = parser.parse(page)['data']
    assert 'number of episodes' not in data


def test_episode_number_should_be_an_integer(movie_combined_details):
    page = movie_combined_details('house_middle')
    data = parser.parse(page)['data']
    assert data['episode number'] == 175


def test_episode_number_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('house')
    data = parser.parse(page)['data']
    assert 'episode number' not in data


def test_previous_episode_should_be_an_imdb_id(movie_combined_details):
    page = movie_combined_details('house_middle')
    data = parser.parse(page)['data']
    assert data['previous episode'] == '2121963'


def test_previous_episode_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('house_first')
    data = parser.parse(page)['data']
    assert 'previous episode' not in data


def test_next_episode_should_be_an_imdb_id(movie_combined_details):
    page = movie_combined_details('house_middle')
    data = parser.parse(page)['data']
    assert data['next episode'] == '2121965'


def test_next_episode_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('house_last')
    data = parser.parse(page)['data']
    assert 'next episode' not in data


def test_episode_of_series_should_have_title_year_and_kind(movie_combined_details):
    page = movie_combined_details('house_middle')
    data = parser.parse(page)['data']
    series = data['episode of']
    assert series.movieID == '0412142'
    assert series.data == {'title': 'House M.D.', 'year': 2004, 'kind': 'tv series'}


def test_episode_of_mini_series_should_have_kind_tv_series(movie_combined_details):
    page = movie_combined_details('band_ep4')
    data = parser.parse(page)['data']
    series = data['episode of']
    assert series.movieID == '0185906'
    assert series.data == {'title': 'Band of Brothers', 'year': 2001, 'kind': 'tv series'}


def test_episode_of_series_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('house')
    data = parser.parse(page)['data']
    assert 'episode of' not in data


def test_rating_should_be_between_1_and_10(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert 1.0 <= data['rating'] <= 10.0


def test_rating_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('ates_parcasi')
    data = parser.parse(page)['data']
    assert 'rating' not in data


def test_votes_should_be_an_integer(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['votes'] > 1000000


def test_votes_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('ates_parcasi')
    data = parser.parse(page)['data']
    assert 'votes' not in data


@mark.fragile
def test_rank_top250_should_be_between_1_and_250(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert 1 <= data['top 250 rank'] <= 250


@mark.fragile
def test_rank_bottom100_should_be_between_1_and_100(movie_combined_details):
    page = movie_combined_details('manos')
    data = parser.parse(page)['data']
    assert 1 <= data['bottom 100 rank'] <= 100


def test_rank_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('ates_parcasi')
    data = parser.parse(page)['data']
    assert 'top 250 rank' not in data
    assert 'bottom 100 rank' not in data


@mark.fragile
def test_series_season_titles_should_be_a_list_of_season_titles(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert data['seasons'] == [str(i) for i in range(1, 12)] + ['unknown']


def test_series_season_titles_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert 'seasons' not in data


def test_series_number_of_seasons_numeric_should_be_ok(movie_combined_details):
    page = movie_combined_details('house')
    data = parser.parse(page)['data']
    assert data['number of seasons'] == 8


@mark.fragile
def test_series_number_of_seasons_should_exclude_non_numeric_season_titles(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert data['number of seasons'] == 11


def test_original_air_date_should_be_a_date(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert data['original air date'] == '9 June 2007'


def test_original_air_date_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert 'original air date' not in data


def test_season_and_episode_numbers_should_be_integers(movie_combined_details):
    page = movie_combined_details('dr_who_blink')
    data = parser.parse(page)['data']
    assert data['season'] == 3
    assert data['episode'] == 10


def test_season_and_episode_numbers_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('dr_who')
    data = parser.parse(page)['data']
    assert 'season' not in data
    assert 'episode' not in data


def test_genres_single_should_be_a_list_of_genre_names(movie_combined_details):
    page = movie_combined_details('if')
    data = parser.parse(page)['data']
    assert data['genres'] == ['Drama']


def test_genres_multiple_should_be_a_list_of_genre_names(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['genres'] == ['Action', 'Sci-Fi']


# TODO: find a movie with no genre
# def test_genres_none_should_be_excluded(movie_combined_details):
#     page = get_page(movie_combined_details, '???')
#     data = parser.parse(page)['data']
#     assert 'genres' not in data


def test_plot_outline_should_be_a_longer_text(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert re.match('^A computer hacker .* against its controllers.$', data['plot outline'])


def test_plot_outline_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('ates_parcasi')
    data = parser.parse(page)['data']
    assert 'plot outline' not in data


def test_mpaa_should_be_a_rating(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['mpaa'] == 'Rated R for sci-fi violence and brief language'


def test_mpaa_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('ates_parcasi')
    data = parser.parse(page)['data']
    assert 'mpaa' not in data


def test_runtimes_single_should_be_a_list_in_minutes(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['runtimes'] == ['136']


def test_runtimes_with_countries_should_include_context(movie_combined_details):
    page = movie_combined_details('suspiria')
    data = parser.parse(page)['data']
    assert data['runtimes'] == ['98', 'Germany:88', 'USA:92', 'Argentina:95']


def test_runtimes_multiple_with_notes_should_include_notes(movie_combined_details):
    page = movie_combined_details('shining')
    data = parser.parse(page)['data']
    assert data['runtimes'] == [
        '144::(cut)',
        '119::(cut) (European version)',
        '146::(original version)',
        'USA:142::(US dvd release: B002VWNIDG)'
    ]


def test_runtimes_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('matrix_vg')
    data = parser.parse(page)['data']
    assert 'runtimes' not in data


def test_countries_single_should_be_a_list_of_country_names(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['countries'] == ['USA']


def test_countries_multiple_should_be_a_list_of_country_names(movie_combined_details):
    page = movie_combined_details('shining')
    data = parser.parse(page)['data']
    assert data['countries'] == ['UK', 'USA']


# TODO: find a movie with no country
# def test_countries_none_should_be_excluded(movie_combined_details):
#     page = get_page(movie_combined_details, '???')
#     data = parser.parse(page)['data']
#     assert 'countries' not in data


def test_country_codes_single_should_be_a_list_of_country_codes(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['country codes'] == ['us']


def test_country_codes_multiple_should_be_a_list_of_country_codes(movie_combined_details):
    page = movie_combined_details('shining')
    data = parser.parse(page)['data']
    assert data['country codes'] == ['gb', 'us']


# TODO: find a movie with no country
# def test_country_codes_none_should_be_excluded(movie_combined_details):
#     page = get_page(movie_combined_details, '???')
#     data = parser.parse(page)['data']
#     assert 'country codes' not in data


def test_languages_single_should_be_a_list_of_language_names(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['languages'] == ['English']


def test_languages_multiple_should_be_a_list_of_language_names(movie_combined_details):
    page = movie_combined_details('ace_in_the_hole')
    data = parser.parse(page)['data']
    assert data['languages'] == ['English', 'Spanish', 'Latin']


def test_languages_single_none_as_a_language_name_should_be_valid(movie_combined_details):
    page = movie_combined_details('matrix_short')
    data = parser.parse(page)['data']
    assert data['languages'] == ['None']


# TODO: find a movie with no language
# def test_languages_none_should_be_excluded(movie_combined_details):
#     url = get_url(TITLE_COMBINED_URL, '???')
#     data = scrape(page, imdb[MOVIE_COMBINED], content_format='html')
#     assert 'languages' not in data


def test_language_codes_single_should_be_a_list_of_language_names(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['language codes'] == ['en']


def test_language_codes_multiple_should_be_a_list_of_language_names(movie_combined_details):
    page = movie_combined_details('ace_in_the_hole')
    data = parser.parse(page)['data']
    assert data['language codes'] == ['en', 'es', 'la']


def test_language_codes_single_none_as_a_language_name_should_be_valid(movie_combined_details):
    page = movie_combined_details('matrix_short')
    data = parser.parse(page)['data']
    assert data['language codes'] == ['zxx']


# TODO: find a movie with no language
# def test_language_codes_none_should_be_excluded(movie_combined_details):
#     url = get_url(TITLE_COMBINED_URL, '???')
#     data = scrape(page, imdb[MOVIE_COMBINED], content_format='html')
#     assert 'language codes' not in data


def test_colors_single_should_be_a_list_of_color_types(movie_combined_details):
    page = movie_combined_details('matrix')
    data = parser.parse(page)['data']
    assert data['color info'] == ['Color']


def test_colors_multiple_should_be_a_list_of_color_types(movie_combined_details):
    page = movie_combined_details('pleasantville')
    data = parser.parse(page)['data']
    assert data['color info'] == ['Black and White', 'Color']


def test_colors_with_notes_single_should_include_notes(movie_combined_details):
    page = movie_combined_details('manos')
    data = parser.parse(page)['data']
    assert data['color info'] == ['Color::(Eastmancolor)']


def test_colors_with_notes_multiple_should_include_notes(movie_combined_details):
    page = movie_combined_details('if')
    data = parser.parse(page)['data']
    assert data['color info'] == ['Black and White', 'Color::(Eastmancolor) (uncredited)']


def test_colors_none_should_be_excluded(movie_combined_details):
    page = movie_combined_details('matrix_tv')
    data = parser.parse(page)['data']
    assert 'color info' not in data
