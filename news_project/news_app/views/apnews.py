from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

class FetchNewsView(APIView):

    def get(self, request):
        url = request.GET.get('url', 'https://apnews.com/')
        news_data = fetch_latest_news(url)

        response = {
            "news_data": news_data
        }

        return Response(response, status=status.HTTP_200_OK)

def fetch_latest_news(url):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = []
    news_items = soup.find_all('div', class_='PageList-items')

    for item in news_items:
        headline_tag = item.find('h3', class_='PagePromo-title')
        headline = headline_tag.get_text(strip=True) if headline_tag else None

        summary_tag = item.find('div', class_='PagePromo')
        summary = summary_tag.get_text(strip=True) if summary_tag else None

        link_tag = item.find('a', href=True)
        link = link_tag['href'] if link_tag else None

        if link:
            news_details = fetch_news_details1(link)
            articles.append({
                'Headline': headline,
                'Summary': summary,
                'Link': link,
                'Detailed Content': news_details
            })
        else:
            articles.append({
                'Headline': headline,
                'Summary': summary,
                'Link': link
            })

    return articles

def fetch_news_details1(url):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    headline_tag = soup.find('h1', class_='sp-ttl')
    headline = headline_tag.get_text(strip=True) if headline_tag else 'N/A'

    content_tags = soup.find_all('p')
    content = ' '.join([tag.get_text(strip=True) for tag in content_tags])

    date_tag = soup.find('div', class_='dateline')
    publication_date = date_tag.get_text(strip=True) if date_tag else 'N/A'

    author_tag = soup.find('span', class_='pst-by')
    author = author_tag.get_text(strip=True) if author_tag else 'N/A'

    article_data = {
        'Headline': headline,
        'Content': content,
        'Publication Date': publication_date,
        'Author': author,
        'URL': url
    }

    return article_data
