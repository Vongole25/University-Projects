from llm_ss.dataset import map_candidates_from_row


def test_map_candidates_handles_shuffled_gold_label_order():
    row = {
        "sentences": {
            "gold_label": ["unrelated", "stereotype", "anti-stereotype"],
            "sentence": ["C", "A", "B"],
        }
    }

    mapped = map_candidates_from_row(row)

    assert mapped == {
        "stereotype": "A",
        "anti-stereotype": "B",
        "unrelated": "C",
    }
