import ckan.model as model
from sqlalchemy import Column, types
from sqlalchemy.ext.declarative import declarative_base
import json
import uuid
from datetime import datetime

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = 'blog_post'
    
    id = Column(types.UnicodeText, primary_key=True)
    title = Column(types.UnicodeText, nullable=False)
    content = Column(types.UnicodeText, nullable=False)
    author = Column(types.UnicodeText, nullable=False)
    thumbnail = Column(types.UnicodeText, nullable=True)
    images = Column(types.UnicodeText, nullable=True)  # JSON array of image paths
    created = Column(types.DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(types.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, **kwargs):
        super(BlogPost, self).__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def to_dict(self):
        """Convert model to dictionary"""
        images_list = []
        if self.images:
            try:
                images_list = json.loads(self.images)
            except:
                images_list = []
        
        created_str = None
        if self.created:
            if isinstance(self.created, str):
                created_str = self.created
            else:
                created_str = self.created.strftime('%Y-%m-%d')
        
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'thumbnail': self.thumbnail,
            'images': images_list,
            'created': created_str,
            'updated': self.updated.strftime('%Y-%m-%d') if self.updated and not isinstance(self.updated, str) else self.updated
        }

