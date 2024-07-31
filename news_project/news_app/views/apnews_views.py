
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import ApNewsModel
from ..serializers import ApNewsSerializer
import requests
from bs4 import BeautifulSoup
import uuid

class ApNewsViewSet(viewsets.ModelViewSet):
    queryset = ApNewsModel.objects.all()
    serializer_class = ApNewsSerializer

    @action(detail=False, methods=['get'])
    def fetch_news(self, request):
        url = request.GET.get('url', 'https://apnews.com/')
        news_data = self.fetch_latest_news(url)

        response_data = []
        for article in news_data:
            # Generate a unique _id for each article
            unique_id = str(uuid.uuid4())

            obj, created = ApNewsModel.objects.update_or_create(
                _id=unique_id,  # Use the generated unique _id
                defaults={
                    'headline': article['Headline'],
                    'summary': article.get('Summary'),
                    'link': article.get('Link'),
                    'url': article.get('URL'),
                    'image':article.get('Image')
                }
            )
            response_data.append({
                '_id': obj._id,  # Return the _id field
                'Headline': obj.headline,
                'Summary': obj.summary,
                'Image':obj.image,
                'Link': obj.link,
                # 'URL': obj.url
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def fetch_latest_news(self, url):
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

            image_tag = item.find('img', class_='Image')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_news_details1(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image':image,
                    'URL': news_details['URL'],
                    'ExternalID': external_id  # Pass the unique identifier
                })
            else:
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'ExternalID': external_id  # Pass the unique identifier
                })

        return articles

    def fetch_news_details1(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        headline_tag = soup.find('h1', class_='sp-ttl')
        headline = headline_tag.get_text(strip=True) if headline_tag else 'N/A'

        article_data = {
            'Headline': headline,
            'URL': url
        }

        return article_data
