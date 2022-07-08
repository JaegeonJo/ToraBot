import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://tgd.kr/s/{0}'

def get_article_id(article):
    return article.attrs['href'].split('/')[-1]

def get_available_categories(streamer_id):
    """
    Get list of available categories from tgd.kr/s/{streamer_id}

    params:
        streamer_id(string): Target streamer ID for crawling

    returns:
        List[string]
    """
    url = BASE_URL.format(streamer_id)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    category_elems = soup.select('div #article-list-category a')
    categories = [elem.text for elem in category_elems if elem.text.strip()]
    return categories

def get_new_articles(streamer_id, last_update='0'):
    """
    Get new articles from tgd.kr/s/{streamer_id}

    params:
        streamer_id(string): Target streamer ID for crawling
        last_update(string): Aritcles that has greater article id than last_update will be returned.

    returns:
        List[dict]
        dictionary format:
            {
                "category": string,
                "title": string,
                "article_id": string
            }  
    """
    url = BASE_URL.format(streamer_id)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    categories = soup.select('div.article-list-row.has-category div.list-title .category')
    articles = soup.select('div.article-list-row.has-category div.list-title a[href]')
    articles = [atcl for atcl in articles if not 'bold' in atcl.attrs['style']]
    assert len(articles) == len(categories), f"Number of articles and categories are different, {len(articles)} vs {len(categories)}"
    new_article_idx = []
    for i, article in enumerate(articles):
        article_id = get_article_id(article)
        if article_id > last_update:
            new_article_idx.append(i)
    new_articles = []
    for idx in new_article_idx:
        category = categories[idx].text.strip()
        title = articles[idx].attrs['title']
        article_id = get_article_id(articles[idx])
        new_article = {
            "category": category,
            "title": title,
            "article_id": article_id
        }
        new_articles.append(new_article)
    new_articles.sort(key=lambda x: x['article_id'])
    return new_articles


