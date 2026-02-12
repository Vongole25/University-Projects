from pathlib import Path


def test_readme_has_no_hf_token_like_string():
    readme = Path(__file__).resolve().parents[1] / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert "hf_" not in text
