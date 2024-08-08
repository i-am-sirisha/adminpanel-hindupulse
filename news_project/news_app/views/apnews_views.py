from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import StagingApNewsModel
from ..serializers import StagingApNewsSerializer
import requests
from bs4 import BeautifulSoup
import uuid
from urllib.parse import urljoin

class ApNewsViewSet(viewsets.ModelViewSet):
    queryset = StagingApNewsModel.objects.all()
    serializer_class = StagingApNewsSerializer

    @action(detail=False, methods=['get'])
    def fetch_news(self, request=None):
        urls = request.GET.getlist('url', [
            'https://apnews.com/', 'https://www.cnbc.com/world/?region=world',
            'https://www.news24.com/', 'https://www.nbcnews.com/', 'https://www.abc.net.au/news/justin',
            'https://www.bbc.com/news', 'https://edition.cnn.com/world', 'https://www.aljazeera.com',
            'https://asia.nikkei.com/', 'https://www.euronews.com/just-in', 'https://www.ft.com/world',
            'https://timesofindia.indiatimes.com/','https://www.scmp.com/live?module=oneline_menu_section_int&pgtype=homepage',
            'https://www.nytimes.com/section/world','https://allafrica.com/'
        ]) if request else [
            'https://apnews.com/', 'https://www.cnbc.com/world/?region=world',
            'https://www.news24.com/', 'https://www.nbcnews.com/', 'https://www.abc.net.au/news/justin',
            'https://www.bbc.com/news', 'https://edition.cnn.com/world', 'https://www.aljazeera.com',
            'https://asia.nikkei.com/', 'https://www.euronews.com/just-in', 'https://www.ft.com/world',
            'https://timesofindia.indiatimes.com/','https://www.scmp.com/live?module=oneline_menu_section_int&pgtype=homepage',
            'https://www.nytimes.com/section/world','https://allafrica.com/'
        ]

        all_news_data = []

        for url in urls:
            fetch_method = getattr(self, f'fetch_{self.get_source_name(url)}', None)
            if fetch_method:
                news_data = fetch_method(url)
                if news_data is not None:
                    print(f"{self.get_source_name(url).upper()} News Data:")
                    all_news_data.extend(news_data)
                else:
                    print(f"No data returned from {self.get_source_name(url).upper()}")

        response_data = self.process_news_data(all_news_data)
        return Response(response_data, status=status.HTTP_200_OK)

    def get_source_name(self, url):
        sources = {
            'apnews.com': 'apnews',
            'cnbc.com': 'cbncnews',
            'news24.com': 'news24',
            'nbcnews.com': 'nbcnews',
            'abc.net.au': 'abcnews',
            'bbc.com': 'bbcnews',
            'cnn.com': 'cnnnews',
            'aljazeera.com': 'aljazeera',
            'asia.nikkei.com': 'asianikkei',
            'euronews.com': 'euronews',
            'ft.com': 'ftnews',
            'timesofindia.indiatimes.com':'timesofindianews',
            'scmp.com':'scmpnews',
            'nytimes.com':'nytimesnews',
            'allafrica.com':'allafricanews'
        }
        for key, value in sources.items():
            if key in url:
                return value
        return 'unknown'

    def process_news_data(self, all_news_data):
        response_data = []
        for article in all_news_data:
            headline = article.get('Headline')
            summary = article.get('Summary')

            # Check if at least one of Headline or Summary is present
            if headline or summary:
                unique_id = str(uuid.uuid4())
                obj, created = StagingApNewsModel.objects.update_or_create(
                    _id=unique_id,
                    defaults={
                        'headline': headline,
                        'summary': summary,
                        'link': article.get('Link'),
                        'url': article.get('URL'),
                        'image': article.get('Image')
                    }
                )
                response_data.append({
                    '_id': obj._id,
                    'Headline': obj.headline,
                    'Summary': obj.summary,
                    'Image': obj.image,
                    'Link': obj.link
                })
        return response_data

    def fetch_apnews(self, url):
        return self.fetch_news_from_site(url, 'div', 'PageList-items', 'h3', 'PagePromo-title', 'div', 'PagePromo', 'img', 'Image', 'a', 'href')

    def fetch_cbncnews(self, url):
        return self.fetch_news_from_site(url, 'div', 'Card-standardBreakerCard', 'a', 'Card-title', 'div', 'PagePromo', 'img', 'Card-mediaContainerInner', 'a', 'href')

    def fetch_news24(self, url):
        return self.fetch_news_from_site(url, 'div', 'article-list tf-grid', 'div', 'article-item__title', 'div', 'PagePromo', 'div', 'article-item__image img', 'a', 'href')

    def fetch_nbcnews(self, url):
        return self.fetch_news_from_site(url, 'li', 'styles_item__1iZnY', 'h2', 'styles_teaseTitle__H4OWQ', 'div', 'PagePromo', 'a', 'Media_imageOverlayLink__VRlFS Media_linkedImage__d5Udf', 'a', 'href')

    def fetch_abcnews(self, url):
        return self.fetch_news_from_site(url, 'div', 'CardList_gridItem__aujmN', 'h3', 'CardHeading_cardHeading__FpsU_', 'div', 'GenericCard_synopsis__mgnzs', 'img', 'Image_image__5tFYM', 'a', 'href')

    def fetch_bbcnews(self, url):
        return self.fetch_news_from_site(url, 'div', 'sc-35aa3a40-2 cVXNac', 'h2', 'sc-4fedabc7-3 zTZri', 'p', 'sc-b8778340-4 kYtujW', 'img', 'sc-814e9212-0 hIXOPW', 'a', 'href')

    def fetch_cnnnews(self, url):
        return self.fetch_news_from_site(url, 'div', 'container__field-links container_lead-plus-headlines__field-links', 'span', 'container__headline-text', 'div', 'PagePromo', 'img', 'image__dam-img', 'a', 'href')

    def fetch_aljazeera(self, url):
        return self.fetch_news_from_site(url, 'li', 'hp-featured-second-stories__item', 'h3', 'article-card__title', 'div', 'PagePromo', 'div', 'article-card__image-wrap article-card__featured-image', 'a', 'href')
    
    def fetch_asianikkei(self, url):
        return self.fetch_news_from_site(url, 'div', 'landing-page__block block_collection', 'a', 'article-block__primary-tag', 'span', 'ezstring-field', 'img', 'img-fluid', 'a', 'href')    
    
    def fetch_euronews(self, url):
        return self.fetch_news_from_site(url, 'li', 'js-timeline-item', 'h3', 'm-object__title', 'div', 'm-object__description', 'img', 'm-img', 'a', 'href')
 
    def fetch_ftnews(self, url):
        return self.fetch_news_from_site(url, 'li', 'o-teaser-collection__item', 'div', 'o-teaser__heading', 'p', 'o-teaser__standfirst', 'img', 'o-teaser__image', 'a', 'href')
    
    def fetch_timesofindianews(self, url):
        return self.fetch_news_from_site(url, 'div', 'col_l_6', 'figcaption', '', 'h2', 'sortDec', 'img', 'thumb', 'a', 'href')
    
    def fetch_scmpnews(self, url):
        return self.fetch_news_from_site(url,'div', 'e1ofzbgq6 css-1wydqy6 e10emkcr6',  'span', 'css-0 e298i0d2','p', 'css-onn2v5 e1nmpk500','img', 'css-1s0st0y e445x7d0','a', 'href')
    def fetch_allafricanews(self, url):
        return self.fetch_news_from_site(url,'div', 'row no-gutter items',  'span', 'headline','p', 'teaser-image-large_paragraph text-block','img', 'img-responsive','a', 'href')
    def fetch_nytimesnews(self, url):
        return self.fetch_news_from_site(url,'li', 'css-18yolpw','h3', 'css-1j88qqx e15t083i0','p', 'css-1pga48a e15t083i1','img', 'css-rq4mmj','a', 'href')
    

    def fetch_news_from_site(self, url, container_tag, container_class, headline_tag, headline_class, summary_tag, summary_class, image_tag, image_class, link_tag, link_attr):
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            news_items = soup.find_all(container_tag, class_=container_class)
            print(f"Found news items: {len(news_items)}")

            for item in news_items:
                headline = item.find(headline_tag, class_=headline_class)
                summary = item.find(summary_tag, class_=summary_class)
                image = item.find(image_tag, class_=image_class)
                link = item.find(link_tag)
                
                if headline:
                    headline_text = headline.get_text(strip=True)
                else:
                    headline_text = None

                if summary:
                    summary_text = summary.get_text(strip=True)
                else:
                    summary_text = None

                if image:
                    image_url = image['src']
                else:
                    image_url = None

                if link:
                    link_url = link[link_attr]
                else:
                    link_url = None

                articles.append({
                    'Headline': headline_text,
                    'Summary': summary_text,
                    'Image': image_url,
                    'Link': link_url,
                    'URL': url
                })
                
            return articles
        
        except Exception as e:
            print(f"Error fetching news from {url}: {e}")
            return []



