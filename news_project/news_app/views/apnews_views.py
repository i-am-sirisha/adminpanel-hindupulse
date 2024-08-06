
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import StagingApNewsModel
from ..serializers import StagingApNewsSerializer
import requests
from bs4 import BeautifulSoup
import uuid

class ApNewsViewSet(viewsets.ModelViewSet):
    queryset = StagingApNewsModel.objects.all()
    serializer_class = StagingApNewsSerializer

    @action(detail=False, methods=['get'])
    def fetch_news(self, request=None):
        # Call the core method with URLs
        self.process_news(request)

        if request:
            return Response({"status": "News fetched and processed."})

    def process_news(self, request):
        # Use a default URL list if request is None
        urls = request.GET.getlist('url', ['https://apnews.com/', 'https://www.cnbc.com/world/?region=world', 'https://www.news24.com/', 'https://www.nbcnews.com/','https://www.abc.net.au/news','https://www.bbc.com/news','https://edition.cnn.com/world','https://www.aljazeera.com','https://asia.nikkei.com/','https://www.euronews.com/just-in']) if request else ['https://apnews.com/', 'https://www.cnbc.com/world/?region=world', 'https://www.news24.com/', 'https://www.nbcnews.com/','https://www.abc.net.au/news','https://www.bbc.com/news','https://edition.cnn.com/world','https://www.aljazeera.com','https://asia.nikkei.com/','https://www.euronews.com/just-in']

   
        all_news_data = []

        for url in urls:
            if 'apnews.com' in url:
                news_data = self.fetch_apnews(url)
                print("AP News Data:")
            elif 'cnbc.com' in url:
                news_data = self.fetch_cbncnewswebsite(url)
                print("CNBC News Data:")
            elif 'news24.com' in url:
                news_data = self.fetch_news24website(url)
                print("NEWS24 News Data:")
            elif 'nbcnews.com' in url:
                news_data = self.fetch_NbcNewswebsite(url)
                print("Nbc News Data:")
            elif 'abc.net.au' in url:
                news_data = self.fetch_AbcNewswebsite(url)
                print("Abc News Data:")
            elif 'bbc.com' in url:
                news_data = self.fetch_bbcnewswebsite(url)
                print("BBC News Data:")
            elif 'cnn.com' in url:
                news_data = self.fetch_cnnnews(url)
                print('CNN News Data:')
            elif 'aljazeera.com' in url:
                news_data = self.fetch_aljazeeranews(url)
                print('ALJAZEERA News Data:')
        
            elif 'asia.nikkei.com' in url:
                news_data = self.fetch_asianikkeinews(url)
                print('ASIA.NIKKEI News Data:')
            elif 'euronews.com' in url:
                news_data = self.fetch_euronews(url)
                print('euronews News Data:')
            else:
                continue

            all_news_data.extend(news_data)

        response_data = []
        for article in all_news_data:
            # Generate a unique _id for each article
            unique_id = str(uuid.uuid4())

            obj, created = StagingApNewsModel.objects.update_or_create(
                _id=unique_id,  # Use the generated unique _id
                defaults={
                    'headline': article['Headline'],
                    'summary': article.get('Summary'),
                    'link': article.get('Link'),
                    'url': article.get('URL'),
                    'image': article.get('Image')
                }
            )
            response_data.append({
                '_id': obj._id,  # Return the _id field
                'Headline': obj.headline,
                'Summary': obj.summary,
                'Image': obj.image,
                'Link': obj.link,
                # 'URL': obj.url
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def fetch_apnews(self, url):
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
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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

    def fetch_cbncnewswebsite(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('div', class_='Card-standardBreakerCard')

        for item in news_items:
            headline_tag = item.find('a', class_='Card-title')
            headline = headline_tag.get_text(strip=True) if headline_tag else None

            summary_tag = item.find('div', class_='PagePromo')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('img', class_='Card-mediaContainerInner')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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
    
    def fetch_news24website(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('div', class_='article-list tf-grid')
        # print("88888888888888888",news_items)

        for item in news_items:
            headline_tag = item.find('div', class_='article-item__title')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print("jjjjjjjjjjj",headline)

            summary_tag = item.find('div', class_='PagePromo')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('div', class_='article-item__image').find('img')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print("llllllllllll",image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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
    
    def fetch_NbcNewswebsite(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('li', class_='styles_item__1iZnY')
        # print("kkkkkkkkkkkkkkkkkkkkkkkk",news_items)

        for item in news_items:
            headline_tag = item.find('h2', class_='styles_teaseTitle__H4OWQ')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print("111111111111",headline)

            summary_tag = item.find('div', class_='PagePromo')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('a', class_='Media_imageOverlayLink__VRlFS Media_linkedImage__d5Udf')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print("22222222222222",image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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
    

     
    def fetch_AbcNewswebsite(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('li', class_='')

        for item in news_items:
            headline_tag = item.find('h3', class_='Typography_base__sj2RP')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print("111111111111111111111111111111111111",headline)

            summary_tag = item.find('div', class_='VolumeCard_synopsis__IWGFK')
            summary = summary_tag.get_text(strip=True) if summary_tag else None
            # print("2222222222222222222222222222222222222",summary)

            image_tag = item.find('img', class_='Image_image__5tFYM')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print("33333333333333333333333333333333333333333333",image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            # Construct the full URL if the link is relative
            if link and not link.startswith('http'):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            articles.append({
                'Headline': headline,
                'Summary': summary,
                'Link': link,
                'Image': image,
                'ExternalID': external_id  # Pass the unique identifier
            })

            # Optionally, fetch additional article details if needed
            # if link:
            #     news_details = self.fetch_article_details(link)
            #     articles[-1].update({
            #         'URL': news_details.get('URL', link)  # Update with additional details
            #     })

        return articles
    
    def fetch_bbcnewswebsite(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('div', class_='sc-35aa3a40-2 cVXNac')
        # print('llllll',news_items)

        for item in news_items:
            headline_tag = item.find('h2', class_='sc-4fedabc7-3 zTZri')
            headline = headline_tag.get_text(strip=True) if headline_tag else None

            summary_tag = item.find('p', class_='sc-b8778340-4 kYtujW')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('img', class_='sc-814e9212-0 hIXOPW')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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
    
    def fetch_cnnnews(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('div', class_='container__field-links container_lead-plus-headlines__field-links')
        # print("$$$$$$$$$$",news_items)

        for item in news_items:
            headline_tag = item.find('span', class_='container__headline-text')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print("********",headline)

            summary_tag = item.find('div', class_='PagePromo')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('img', class_='image__dam-img')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print("NNNNNNNNNN",image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
                    'URL': news_details['URL'],
                    'ExternalID': external_id
                })
            else:
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'ExternalID': external_id
                })

        return articles

    def fetch_aljazeeranews(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('li', class_='hp-featured-second-stories__item')
        # print("aaaaaaaaaaa",news_items)

        for item in news_items:
            headline_tag = item.find('h3', class_='article-card__title')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print("jjjjjjjj",headline)

            summary_tag = item.find('div', class_='PagePromo')
            summary = summary_tag.get_text(strip=True) if summary_tag else None

            image_tag = item.find('div', class_='article-card__image-wrap article-card__featured-image')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print("hhhhhhhh",image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
                    'URL': news_details['URL'],
                    'ExternalID': external_id
                })
            else:
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'ExternalID': external_id
                })

        return articles



    def fetch_asianikkeinews(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('div', class_='landing-page__block block_collection')
        # print('99999999999',news_items)

        for item in news_items:
            headline_tag = item.find('a', class_='article-block__primary-tag')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            # print('000000000000',headline)

            summary_tag = item.find('span', class_='ezstring-field')
            summary = summary_tag.get_text(strip=True) if summary_tag else None
            # print('444444444',summary)

            image_tag = item.find('img', class_='img-fluid')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            # print('11111111111',image)

            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else None

            if link and not link.startswith(('http://', 'https://')):
                link = requests.compat.urljoin(url, link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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
    
    def fetch_euronews(self, url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        articles = []
        news_items = soup.find_all('li', class_='js-timeline-item')

        for item in news_items:
            headline_tag = item.find('h3', class_='m-object__title')
            headline = headline_tag.get_text(strip=True) if headline_tag else None
            print("11111111111111111111111111111111111111111111",headline)

            summary_tag = item.find('div', class_='m-object__description')
            summary = summary_tag.get_text(strip=True) if summary_tag else None
            print("2222222222222222222222222222222222",summary)

            image_tag = item.find('img', class_='m-img')
            image = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None
            print("33333333333333333333333333333333333333",image)

            link_tag = item.find('a', class_='m-object__title__link')
            link = link_tag['href'] if link_tag else None
            print("4444444444444444444444444444444444444",link)

            # Generate a unique URL-based identifier or use another method if necessary
            external_id = link or str(uuid.uuid4())

            if link:
                news_details = self.fetch_article_details(link)
                articles.append({
                    'Headline': headline,
                    'Summary': summary,
                    'Link': link,
                    'Image': image,
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



    def fetch_article_details(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            headline_tag = soup.find('h1', class_='sp-ttl')
            headline = headline_tag.get_text(strip=True) if headline_tag else 'N/A'

            article_data = {
                'Headline': headline,
                'URL': url
            }

            return article_data
        except requests.exceptions.RequestException as e:
            # Handle specific exceptions if necessary
            print(f"An error occurred: {e}")
            return {
                'Headline': 'N/A',
                'URL': url,
                'Error': str(e)
            }




