"""Test the efficiency of JSON deserialization."""
import json
import timeit

from spnkr.api.authorities.stats.models import MatchHistoryResponse


def main():
    """Test the efficiency of JSON deserialization."""
    with open("api_examples/json/stats/get_match_history.json", "r") as fp:
        data = fp.read()

    def test():
        """Test function."""
        MatchHistoryResponse.from_dict(json.loads(data))

    print(timeit.timeit(test, number=10000), "seconds")


if __name__ == "__main__":
    main()
