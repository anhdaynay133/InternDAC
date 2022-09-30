# Declare libraries
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

# Declare link website crawl
BASE_URL = "https://tuoitre.vn"


# Function to extract html document from given url
def get_html_document(url) -> BeautifulSoup:
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup


# Function to add data to existing json file
def process_data_to_final(file_final, collect_data) -> None:
    # crawl daily add file json
    with open(file_final, 'r+', encoding='utf-8-sig', errors='ignore') as file:
        data = json.load(file)
        if collect_data not in data:
            data.append(collect_data)
            file.seek(0)
            json.dump(data, file, indent=4, ensure_ascii=False)


# Initialize main function containing all information
def main() -> None:
    print(get_html_document(url))
    keyword = list()
    url = BASE_URL + '/tin-moi-nhat.htm'
    file_final = "data_crawl.json"
    # file_final = "/mnt/d/Python_Code/A1_TRAINING_NongVanToan/Phase1/data_crawl.json"

    soup = get_html_document(url)

    tag_ul = soup.find("ul", attrs={"class": "list-news-content"})
    tag_title = tag_ul.find_all("li")
    for i in tag_title:
        # Get title information
        title_tag = i.find("h3", attrs={"class": "title-news"}).a
        # Get description information
        description_tag = i.find("p", attrs={"class": "sapo"})
        # Get category information
        category_tag = i.find("a", attrs={"class": "category-name fl mgl10 mgb4 uppercase"})
        # Get link
        link = i.find("h3", attrs={"class": "title-news"}).a
        link_post = BASE_URL + link["href"]
        soup_post = get_html_document(link_post)
        # Get tags information
        tags = soup_post.find("ul", attrs={"class": "tags-wrapper"})
        for tag in tags.find_all("li"):
            keyword.append(tag.get_text())
        # Get author information
        author = soup_post.find("div", attrs={"class": "author"}).get_text().strip()
        # Get date information
        date_time = soup_post.find("div", attrs={"class": "date-time"}).get_text().strip("GMT+7").rstrip()
        # Convert to standard form in the database
        date_public = datetime.strptime(date_time, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")

        # Put all data in a tupple
        collect_data = {
            "Title": title_tag.get_text(),
            "Description": description_tag.get_text(),
            "Category": category_tag.get_text(),
            "url": link_post,
            "Keyword": keyword,
            "author": author,
            "date_public": date_public}

        # process_data_to_final(file_final, collect_data)
    # Print when crawl done
    print('Crawl done')


# Calling the main function again
if __name__ == "__main__":
    main()
