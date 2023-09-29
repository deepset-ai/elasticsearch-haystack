import pytest

from elasticsearch_haystack.filters import _normalize_filters

filters_data = [
    (
        {
            "$and": {
                "type": {"$eq": "article"},
                "$or": {"genre": {"$in": ["economy", "politics"]}, "publisher": {"$eq": "nytimes"}},
                "date": {"$gte": "2015-01-01", "$lt": "2021-01-01"},
                "rating": {"$gte": 3},
            }
        },
        {
            "bool": {
                "must": [
                    {"term": {"type": "article"}},
                    {
                        "bool": {
                            "should": [
                                {"terms": {"genre": ["economy", "politics"]}},
                                {"term": {"publisher": "nytimes"}},
                            ]
                        }
                    },
                    {"range": {"date": {"gte": "2015-01-01", "lt": "2021-01-01"}}},
                    {"range": {"rating": {"gte": 3}}},
                ]
            }
        },
    ),
    (
        {
            "$or": [
                {"Type": "News Paper", "Date": {"$lt": "2019-01-01"}},
                {"Type": "Blog Post", "Date": {"$gte": "2019-01-01"}},
            ]
        },
        {
            "bool": {
                "should": [
                    {"match": {"Type": "News Paper"}},
                    {"match": {"Type": "Blog Post"}},
                    {"range": {"Date": {"gte": "2019-01-01", "lt": "2019-01-01"}}},
                ]
            }
        },
    ),
    (
        {
            "$and": {
                "type": {"$eq": "article"},
                "date": {"$gte": "2015-01-01", "$lt": "2021-01-01"},
                "rating": {"$gte": 3},
                "$or": {"genre": {"$in": ["economy", "politics"]}, "publisher": {"$eq": "nytimes"}},
            }
        },
        {
            "bool": {
                "must": [
                    {"term": {"type": "article"}},
                    {
                        "bool": {
                            "should": [
                                {"terms": {"genre": ["economy", "politics"]}},
                                {"term": {"publisher": "nytimes"}},
                            ]
                        }
                    },
                    {"range": {"date": {"gte": "2015-01-01", "lt": "2021-01-01"}}},
                    {"range": {"rating": {"gte": 3}}},
                ]
            }
        },
    ),
    (
        {
            "type": "article",
            "date": {"$gte": "2015-01-01", "$lt": "2021-01-01"},
            "rating": {"$gte": 3},
            "$or": {"genre": ["economy", "politics"], "publisher": "nytimes"},
        },
        {
            "bool": {
                "must": [
                    {"match": {"type": "article"}},
                    {
                        "bool": {
                            "should": [
                                {"terms": {"genre": ["economy", "politics"]}},
                                {"match": {"publisher": "nytimes"}},
                            ]
                        }
                    },
                    {"range": {"date": {"gte": "2015-01-01", "lt": "2021-01-01"}}},
                    {"range": {"rating": {"gte": 3}}},
                ]
            }
        },
    ),
    ({"text": "A Foo Document 1"}, {'match': {'text': 'A Foo Document 1'}}),
]


@pytest.mark.parametrize("filters, expected", filters_data)
@pytest.mark.unit
def test_normalize_filters(filters, expected):
    result = _normalize_filters(filters)
    assert result == expected
