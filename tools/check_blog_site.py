import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ARTICLE = ROOT / "blog" / "telco-survival-analysis-report.html"
STYLE = ROOT / "assets" / "style.css"
BLOG_IMAGE_DIR = ROOT / "assets" / "images" / "blog" / "telco-survival-analysis"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def assert_no_draft_language(text: str) -> None:
    blocked = ["Project report placeholder", "Coming soon", "placeholder"]
    found = [word for word in blocked if word in text]
    assert not found, f"article exposes draft language: {found}"


def main() -> None:
    index = read(INDEX)
    style = read(STYLE)
    blog_section = between(index, '<section id="blog"', '<section id="work"')

    blog_cards = re.findall(r'class="[^"]*(?<![-\w])card(?![-\w])[^"]*"', blog_section)
    assert len(blog_cards) == 1, "homepage should keep one blog card"
    assert "Coming soon" not in blog_section
    assert "placeholder" not in blog_section.lower()
    assert 'href="blog/telco-survival-analysis-report.html"' in blog_section
    assert ARTICLE.exists(), "blog detail page should exist under blog/"

    article = read(ARTICLE)
    assert_no_draft_language(article)
    for required in [
        "IBM Telco Customer Churn",
        "Kaplan-Meier",
        "Cox Proportional Hazards",
        "Accelerated Failure Time",
        "<pre",
        'class="article-figure"',
    ]:
        assert required in article, f"missing report content: {required}"

    assert '../assets/style.css' in article
    assert '../assets/site.js' in article
    assert '../index.html#blog' in article

    for image in [
        "q2-km-overall.png",
        "q2-km-online-security.png",
        "q2-cox-hazard-ratios.png",
        "q2-aft-coefficients.png",
        "q2-clv-horizon.png",
        "q2-profile-survival.png",
    ]:
        path = BLOG_IMAGE_DIR / image
        rel = f"../assets/images/blog/telco-survival-analysis/{image}"
        assert path.exists(), f"missing blog image asset: {image}"
        assert rel in article, f"article does not reference {image}"

    assert "STZhongsong" in style
    assert ".article-body" in style
    assert ".article-code" in style


if __name__ == "__main__":
    main()
