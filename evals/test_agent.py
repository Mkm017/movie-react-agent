import time
import pytest

from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.models import GeminiModel
from deepeval.test_case import (
    LLMTestCase,
    LLMTestCaseParams,
)

from main import run_agent
from evals.test_cases import TEST_CASES


evaluation_model = GeminiModel(
    model="gemini-2.5-flash",
    temperature=0,
)


movie_recommendation_quality = GEval(
    name="Movie Recommendation Quality",
    criteria=(
        "Evaluate whether the actual output is a relevant movie "
        "recommendation that satisfies all requirements in the input "
        "and expected output. Check genre, release year or year range, "
        "and certification when specified. Also check that the response "
        "clearly explains why the recommended movie matches the request."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    threshold=0.7,
    model=evaluation_model,
)


@pytest.mark.parametrize(
    "case_number, case",
    enumerate(TEST_CASES),
)
def test_movie_agent(case_number, case):

    if case_number > 0:
        time.sleep(30)

    actual_output = run_agent(case["input"])

    test_case = LLMTestCase(
        input=case["input"],
        actual_output=actual_output,
        expected_output=case["expected_output"],
    )

    assert_test(
        test_case,
        [movie_recommendation_quality],
    )