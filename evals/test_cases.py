TEST_CASES = [
    {
        "input": "Recommend a horror movie from the 90s rated R",
        "expected_output": (
            "Recommend a horror movie released between 1990 and 1999 "
            "with an R certification."
        ),
    },
    {
        "input": "Recommend an action movie from the 80s",
        "expected_output": (
            "Recommend an action movie released between 1980 and 1989."
        ),
    },
    {
        "input": "Suggest a comedy movie from the 2000s",
        "expected_output": (
            "Recommend a comedy movie released between 2000 and 2009."
        ),
    },
    {
        "input": (
            "Recommend a PG-13 science fiction movie from the 2010s"
        ),
        "expected_output": (
            "Recommend a science fiction movie released between "
            "2010 and 2019 with a PG-13 certification."
        ),
    },
    {
        "input": (
            "Recommend a thriller movie released between 2005 and 2015"
        ),
        "expected_output": (
            "Recommend a thriller movie released between "
            "2005 and 2015."
        ),
    },
]