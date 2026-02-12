from llm_ss.scorer import build_prefix_and_continuation


def test_intrasentence_blank_replacement_includes_suffix_in_continuation():
    context = "The engineer said BLANK yesterday."
    prefix, continuation = build_prefix_and_continuation(
        subset="intrasentence",
        context=context,
        candidate_text="she was right",
    )

    assert prefix == "The engineer said "
    assert continuation == "she was right yesterday."
