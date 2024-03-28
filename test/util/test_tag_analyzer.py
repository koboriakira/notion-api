from notion_api.util.tag_analyzer import analyze_tags


def test_analyze_tags():
    input = {
        "tags": "test1, test2, test3, test1"
    }

    actual = analyze_tags(args=input)
    assert len(actual) == 3
    assert "test1" in actual
    assert "test2" in actual
    assert "test3" in actual
