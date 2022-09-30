# Declare libraries
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Create table article keyword relationship n to 1 article and keyword
association_table = Table(
    "article_keyword",
    Base.metadata,
    Column("article_id", ForeignKey("article.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keyword.id"), primary_key=True), )


# Create Object Category relationship 1 to n with Object Article
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)
    cates = relationship('Article', back_populates='category')

    def __repr__(self):
        return "<Category(category_name='%s')>" % (self.category_name)


# Create Object Article relationship 1 to n with Object Article Keyword
class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    url = Column(String(200), nullable=False)
    date_public = Column(DateTime, nullable=False)
    author_name = Column(String(100), nullable=False)
    cates_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='cates')
    keywords = relationship('Keyword', secondary=association_table, back_populates='articles')

    def __repr__(self):
        return "<Article(title='%s', url = '%s' , description = '%s', date_public = '%s', author_name = '%s', cates_id = '%s' )>" \
               % (self.title, self.description, self.url, self.date_public, self.author_name, self.cates_id)


# Create table keyword relationship 1 to n with Object Article Keyword
class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword_name = Column(String(200), nullable=False)
    articles = relationship("Article", secondary=association_table, back_populates="keywords")

    def __repr__(self):
        return "<Keyword(keyword='%s')>" % (self.keyword)


# Create an engine that stores data in the local directory's
engine = create_engine('mysql+pymysql://root:1234@localhost/phase1', echo=True)

# Create all tables in the engine. This is equivalent to "Create Table"
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
