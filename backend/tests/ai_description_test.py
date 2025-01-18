from src import ai_description

def test_summarizer():
    # Example usage
    comments = [
        "This website is prone to errors.",
        "The UI of this website is great.",
        "I love the design but it crashes often.",
        "The website is slow and unresponsive.",
        "The navigation is confusing and difficult to use.",
        "The content is well-written and informative.",
        "The website is visually appealing and easy to navigate.",
        "I found the website to be very helpful.",
        "The website is not user-friendly.",
        "The website is outdated and needs a redesign.",
        "The website is full of bugs.",
        "The website is not compatible with my browser.",
        "The website is not accessible to people with disabilities.",
        "The website is not secure.",
        "The website is a scam.",
        "I am very satisfied with this website.",
        "I would recommend this website to others.",
        "I will definitely use this website again.",
        "I am not impressed with this website.",
        "I will not be using this website again."
    ]

    # assert that the summary is less than 30 words
    summary = ai_description.summarize_comments(comments=comments, website="www.youtube.com")
    print(summary)

    assert isinstance(summary, str)
    assert summary != ""
    assert len(summary.split()) <= 30
    
    
if __name__ == "__main__":
    test_summarizer()