import os
import json
import requests

from langchain.tools import Tool


GENRE_MAP = {
    "horror": 27,
    "horror movies": 27,
    "action": 28,
    "comedy": 35,
    "drama": 18,
    "thriller": 53,
    "science fiction": 878,
    "sci-fi": 878,
}


def search_movies(tool_input: str) -> str:
    """
    Expected input:

    {
        "genre": "horror",
        "start_year": 1990,
        "end_year": 1999,
        "certification": "R"
    }
    """

    try:
        data = json.loads(tool_input)

        genre = data["genre"]
        start_year = data["start_year"]
        end_year = data["end_year"]
        certification = data["certification"]

    except Exception:
        return (
            "Invalid input. Expected JSON like:\n"
            '{"genre":"horror","start_year":1990,'
            '"end_year":1999,"certification":"R"}'
        )

    api_key = os.getenv("TMDB_API_KEY")

    if not api_key:
        return "TMDB API key is missing."

    genre_id = GENRE_MAP.get(genre.lower())

    if not genre_id:
        return f"Unsupported genre: {genre}"

    if start_year > end_year:
        return "Invalid year range."

    try:
        response = requests.get(
            "https://api.themoviedb.org/3/discover/movie",
            params={
                "api_key": api_key,
                "with_genres": genre_id,
                "primary_release_date.gte": f"{start_year}-01-01",
                "primary_release_date.lte": f"{end_year}-12-31",
                "certification_country": "US",
                "certification": certification,
                "sort_by": "popularity.desc",
                "vote_count.gte": 500,
            },
            timeout=10,
        )

        response.raise_for_status()

        movies = response.json().get("results", [])

        if not movies:
            return "No matching movies found."

        formatted_movies = []

        for movie in movies[:3]:
            title = movie.get("title", "Unknown")
            year = movie.get("release_date", "")[:4]
            score = movie.get("vote_average", "N/A")
            overview = movie.get("overview", "")

            formatted_movies.append(
                f"{title} ({year}) | "
                f"TMDB Score: {score} | "
                f"Overview: {overview}"
            )

        return (
            "\n=== MATCHING MOVIES ===\n\n"
            + "\n\n".join(formatted_movies)
        )

    except requests.Timeout:
        return "TMDB request timed out."

    except requests.RequestException as e:
        return f"TMDB request failed: {str(e)}"


movie_search_tool = Tool(
    name="movie_search_tool",
    func=search_movies,
    description="""
Search movies from TMDB.

Input MUST be valid JSON.

Example:

{
    "genre": "horror",
    "start_year": 1990,
    "end_year": 1999,
    "certification": "R"
}

Another example:

{
    "genre": "action",
    "start_year": 2000,
    "end_year": 2009,
    "certification": "PG-13"
}
""",
)