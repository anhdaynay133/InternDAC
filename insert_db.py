# Declare
from create_db import Article, Category, Keyword,session
import json

#Create list data 
data_import = []

#Open json file 
f = open(r'D:\Python_Code\A1_TRAINING_NongVanToan\Phase1\data_crawl.json', encoding="utf8")
data = json.load(f)
for i in range(len(data)):
    data_import.append(data[i])


for j in data_import:
    # Add objects article
    article = category = session.query(Article).filter(Article.title == j['Title']).first()
    if not article:
        article = Article(title = j['Title'] ,description = j['Description'], url = j['url'] , date_public = j['date_public'], author_name = j['author'])

    # Add objects category
    category = session.query(Category).filter(Category.category_name == j['Category']).first()
    if not category:
        category = Category(category_name=j['Category'])
        session.add(category)
        
    # Add objects article keyword
    category.cates.append(article)
    session.add(article)

    # Add objects Keyword
    keyword = j['Keyword']
    for k in keyword:
        key = session.query(Keyword).filter(Keyword.keyword_name == k).first()
        if not key:
            key = Keyword(keyword_name = k)
            session.add(key)
    article.keywords.append(key)
    
    #Close the session 
    session.commit()


