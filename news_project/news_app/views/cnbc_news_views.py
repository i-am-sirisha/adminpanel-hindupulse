# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from bs4 import BeautifulSoup

# class FetchCnbcNewsView(APIView):
#     """
#     get:
#     Fetch the latest news from CNBC World.

#     Responses:
#     - 200: Successful response with news data
#     """

#     def get(self, request):
#         url = "https://www.cnbc.com/world/?region=world"
#         news_data = fetch_latest_news(url)

#         response = {
#             "news_data": news_data
#         }

#         return Response(response, status=status.HTTP_200_OK)

# def fetch_latest_news(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     html_content = response.content
#     soup = BeautifulSoup(response.content, "html.parser")

#     # Extract the desired data
#     articles = []
#     for article in soup.find_all("div", class_="Card-standardBreakerCard"):
#         # You may need to update the class names based on the page structure
#         title_tag = article.find("a", class_="Card-title")
#         if title_tag:
#             headline = title_tag.get_text(strip=True)
#             link = title_tag["href"]
#             articles.append({"Headline": headline, "Link": link})

#     # Create a DataFrame from the extracted data
#     return articles
