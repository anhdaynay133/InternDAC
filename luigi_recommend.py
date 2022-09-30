# Declare libraries
import luigi
from bs4 import BeautifulSoup
import requests
import json
from sqlalchemy import select
from create_db import session, Article, Category
from datetime import datetime

# Declare list
data_import = []
keyword = []


# Function to extract html document from given url
def get_html_document(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup


class getCleanData(luigi.Task):
    """
    This class will be responsible for taking data from the input and cleaning
    """

    def output(self):
        """
        Returns the target output for this task.
        In this case, it expects a file to be present in the local file system.
        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("luigi_article.json")

    def run(self):
        """
        1.Open read file input
        2.Crawl data from url input
        3.Write the collected data to the output file
        """
        f = open("input.txt", "r")
        url = f.read()
        soup_post = get_html_document(url)
        # Get title information
        title_tag = soup_post.find("h1", attrs={"class": "article-title"})
        # Get description information
        description_tag = soup_post.find("h2", attrs={"class": "sapo"})
        # Get category information
        div_cates = soup_post.find("div", attrs={"class": "bread-crumbs fl"})
        tag_ul = div_cates.find("ul")
        tag_li = tag_ul.find_all("li")
        for i in tag_li:
            category_tag = i.find('a')
            break
        # Get tags information
        tags = soup_post.find("ul", attrs={"class": "tags-wrapper"})
        for tag in tags.find_all("li"):
            keyword.append(tag.get_text())
        # Get author information
        author = soup_post.find("div", attrs={"class": "author"}).get_text().strip()
        if not author:
            return None
        date_time = soup_post.find("div", attrs={"class": "date-time"}).get_text().strip("GMT+7").rstrip()
        date_public = datetime.strptime(date_time, '%d/%m/%Y %H:%M').strftime("%Y-%m-%d %H:%M")
        # Put all data in a tupple
        collect_data = {
            "Title": title_tag.get_text(),
            "Description": description_tag.get_text(),
            "Category": category_tag.get_text(),
            "Url": url,
            "Keyword": keyword,
            "Author": author,
            "Date_public": date_public
        }
        f.close()
        # Output file
        with self.output().open("w") as f:
            json.dump(collect_data, f, indent=4, ensure_ascii=False)


class importData(luigi.Task):
    """
    This class will have the task of importing data into the database and will have no output
    """
    task_complete = False

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.Get_clean_data`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return getCleanData()

    def complete(self):
        """
        this function initializes to not create output file
        """
        return self.task_complete

    def run(self):
        """
        1. Open file json
        2. Import data from database
        """
        self.task_complete = True
        f = open(r'/mnt/d/Python_Code/A1_TRAINING_NongVanToan/Phase1/luigi_article.json', encoding="utf-8")

        data_import.append(json.load(f))

        for data in data_import:
            article = session.query(Article).filter(Article.title == data['Title']).first()
            if not article:
                article = Article(title=data['Title'], description=data['Description'], url=data['Url'],
                                  date_public=data['Date_public'], author_name=data['Author'])

            # Add objects category
            category = session.query(Category).filter(Category.category_name == data['Category']).first()
            if not category:
                category = Category(category_name=data['Category'])
                session.add(category)

            # Add objects article keyword
            category.cates.append(article)
            session.add(article)
            session.commit()


class recommend(luigi.Task):
    """
    This class will be responsible for writing recommendations for articles in the input file
    """

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.Import_data`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return importData()

    def output(self):
        """
        Returns a text file containing information about related articles
        """
        return luigi.LocalTarget("recommend_output.txt")

    def run(self):
        """
        1. Query the newly added post
        2. Compare the same category with other articles
        3. Export to txt file
        """
        with self.output().open("w") as outfile:
            subquery = select(Article.cates_id).order_by(Article.id.desc()).limit(1).subquery()
            query = session.query(Article.title, Article.url, Category.category_name).join(Category).filter(
                Article.cates_id == subquery).limit(5)
            for row in session.execute(query):
                outfile.write(str(row) + '\n')


if __name__ == "__main__":
    luigi.run()
