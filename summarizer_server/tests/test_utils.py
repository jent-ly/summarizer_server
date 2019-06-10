def get_article1_contents():
    return get_article_contents("article1")

def get_article_contents(article_name):
    article_file_name = "summarizer_server/tests/fixtures/" + article_name + ".txt"
    with open(article_file_name, "r") as f:
        return f.read()

