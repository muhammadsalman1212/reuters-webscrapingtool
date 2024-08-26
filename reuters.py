from datetime import datetime, timedelta
import pandas as pd
import requests
import json
import os

# Enter your search item here
searchitem = ("oil")
firstpage = False

file_path = f'{searchitem}.csv'

if os.path.exists(file_path):
    os.remove(file_path)
    print(f"{file_path} has been deleted successfully.")
else:
    print(f"{file_path} does not exist.")

url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2"

current_date = datetime.now().strftime("%Y-%m-%d")
last_month_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

page = 1
count = 0

# Check if file exists and is empty
file_exists = os.path.isfile(f"{searchitem}.csv")
file_empty = os.stat(f"{searchitem}.csv").st_size == 0 if file_exists else True

while True:
    querystring = {
        "query": json.dumps({
            "end_date": current_date,
            "keyword": searchitem,
            "offset": count,
            "orderby": "relevance",
            "size": 20,
            "start_date": last_month_date,
            "website": "reuters"
        }),
        "d": "209",  # Updated based on the second code snippet
        "_website": "reuters"
    }

    headers = {
        "cookie": "usprivacy=1---; _gcl_au=1.1.429713004.1722093859; ...",  # Full cookie header from second code snippet
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "referer": f"https://www.reuters.com/site-search/?query={searchitem}&date=past_month&sort=relevance&offset=0",
        "sec-ch-device-memory": "8",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-arch": "\"x86\"",
        "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.122\", \"Chromium\";v=\"127.0.6533.122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": "\"\"",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Handle HTTP errors
        data = response.json()

        # Check if 'articles' exists in the response
        if 'result' in data and 'articles' in data['result']:
            articles = data['result']['articles']
            if not articles:
                print("No more articles found.")
                break

            data_list = []
            for article in articles:
                date = article['display_time']
                try:
                    formated_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y")
                except ValueError:
                    formated_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
                print(formated_date)
                data_dict = {
                    'Searched Item': searchitem,
                    'link': "https://www.reuters.com" + article['canonical_url'],
                    'Headline': article['basic_headline'],
                    'date-time': formated_date
                }
                data_list.append(data_dict)

            # Store data in csv
            df = pd.DataFrame(data_list)
            df.to_csv(f"{searchitem}.csv", mode='a+', header=file_empty, index=False)

            # After writing for the first time, set file_empty to False
            if file_empty:
                file_empty = False

            print(f"Data Scraped From {page} Page")
            if firstpage == True:
                break
            count += 20
            page += 1
        else:
            print("No articles found in response.")
            break

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        break
    except Exception as err:
        print(f"Scraping Done. No More Data")
        break





# from datetime import datetime, timedelta
# import pandas as pd
# import requests
# import json
# import os



# # Enter your search item here
# searchitem = "oil"
# firstpage = False





# file_path = f'{searchitem}.csv'

# if os.path.exists(file_path):
#     os.remove(file_path)
#     print(f"{file_path} has been deleted successfully.")
# else:
#     print(f"{file_path} does not exist.")



# url = "https://www.reuters.com/pf/api/v3/content/fetch/articles-by-search-v2"

# current_date = datetime.now().strftime("%Y-%m-%d")
# last_month_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# page = 1
# count = 0

# # Check if file exists and is empty
# file_exists = os.path.isfile(f"{searchitem}.csv")
# file_empty = os.stat(f"{searchitem}.csv").st_size == 0 if file_exists else True

# while True:
#     querystring = {
#         "query": json.dumps({
#             "end_date": current_date,
#             "keyword": searchitem,
#             "offset": count,
#             "orderby": "relevance",
#             "size": 20,
#             "start_date": last_month_date,
#             "website": "reuters"
#         }),
#         "d": "204",
#         "_website": "reuters"
#     }

#     headers = {
#         "accept": "*/*",
#         "accept-language": "en-US,en;q=0.9",
#         "referer": f"https://www.reuters.com/site-search/?query={searchitem}&date=past_month&sort=relevance&offset=0",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
#     }

#     try:
#         response = requests.get(url, headers=headers, params=querystring)
#         response.raise_for_status()  # Handle HTTP errors
#         data = response.json()

#         # Check if 'articles' exists in the response
#         if 'result' in data and 'articles' in data['result']:
#             articles = data['result']['articles']
#             if not articles:
#                 print("No more articles found.")
#                 break

#             data_list = []
#             for article in articles:
#                 date = article['display_time']
#                 try:
#                     formated_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%B %d, %Y")
#                 except ValueError:
#                     formated_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y")
#                 print(formated_date)
#                 data_dict = {
#                     'Searched Item': searchitem,
#                     'link': "https://www.reuters.com" + article['canonical_url'],
#                     'Headline': article['basic_headline'],
#                     'date-time': formated_date
#                 }
#                 data_list.append(data_dict)

#             # Store data in csv
#             df = pd.DataFrame(data_list)
#             # if there is a website named searchitem.csv remove that csv data


#             # Check if the file exists, then delete it


#             # headers = ['Searched Item', 'link', 'Headline', 'date-time']
#             df.to_csv(f"{searchitem}.csv", mode='a+', header=file_empty, index=False)



#             # After writing for the first time, set file_empty to False
#             if file_empty:
#                 file_empty = False

#             print(f"Data Scraped From {page} Page")
#             if firstpage == True:
#                 break
#             count += 20
#             page += 1
#         else:
#             print("No articles found in response.")
#             break

#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred: {http_err}")
#         break
#     except Exception as err:
#         print(f"Scraping Done. No More Data")
#         break
