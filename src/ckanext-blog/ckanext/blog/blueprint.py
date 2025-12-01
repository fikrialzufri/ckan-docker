from flask import Blueprint, render_template, request, redirect, url_for
import ckan.plugins.toolkit as toolkit
import ckan.model as model
import ckan.logic as logic
import ckan.lib.helpers as h
from ckan.common import c, g, _
import os
from werkzeug.utils import secure_filename
import uuid
import json
from ckanext.blog.model import BlogPost

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
check_access = logic.check_access

blog_blueprint = Blueprint('blog', __name__)

def get_upload_folder():
    """Mendapatkan folder untuk menyimpan file upload"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    upload_folder = os.path.join(current_dir, 'public', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

def save_uploaded_file(file, prefix=''):
    """Menyimpan file yang diupload dan mengembalikan path relatif"""
    if not file or not file.filename:
        return None
    
    try:
        filename = secure_filename(file.filename)
        if not filename:
            return None
        
        unique_filename = f"{prefix}_{uuid.uuid4().hex[:8]}_{filename}"
        upload_folder = get_upload_folder()
        file_path = os.path.join(upload_folder, unique_filename)
        
        file.save(file_path)
        
        if os.path.exists(file_path):
            return f"/fanstatic/blog/uploads/{unique_filename}"
        else:
            return None
    except Exception as e:
        import logging
        log = logging.getLogger(__name__)
        log.error(f"Error saving uploaded file: {str(e)}")
        return None

def get_public_url(path):
    """Mengkonversi path file menjadi URL publik"""
    if not path:
        return None
    if path.startswith('http'):
        return path
    if path.startswith('/'):
        return path
    return f"/fanstatic/blog/uploads/{path}"

@blog_blueprint.route('/blog', endpoint='index')
def index():
    """Menampilkan daftar semua post blog"""
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user,
        'auth_user_obj': c.userobj
    }
    
    try:
        posts_query = model.Session.query(BlogPost).order_by(BlogPost.created.desc()).all()
        posts = [post.to_dict() for post in posts_query]
        
        return render_template('blog/index.html', posts=posts)
    except Exception as e:
        h.flash_error(_('Error loading blog posts: %s') % str(e))
        return render_template('blog/index.html', posts=[])

@blog_blueprint.route('/blog/new', methods=['GET', 'POST'], endpoint='new')
def new():
    """Form untuk membuat post blog baru"""
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user,
        'auth_user_obj': c.userobj
    }
    
    try:
        check_access('sysadmin', context)
    except NotAuthorized:
        h.flash_error(_('Not authorized to create blog posts'))
        return redirect(url_for('blog.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        
        thumbnail_path = None
        if 'thumbnail' in request.files:
            thumbnail_file = request.files['thumbnail']
            if thumbnail_file and thumbnail_file.filename:
                thumbnail_path = save_uploaded_file(thumbnail_file, 'thumb')
                if thumbnail_path:
                    import logging
                    log = logging.getLogger(__name__)
                    log.info(f"Thumbnail saved: {thumbnail_path}")
        
        images_paths = []
        if 'images' in request.files:
            image_files = request.files.getlist('images')
            for image_file in image_files:
                if image_file and image_file.filename:
                    img_path = save_uploaded_file(image_file, 'img')
                    if img_path:
                        images_paths.append(img_path)
                        import logging
                        log = logging.getLogger(__name__)
                        log.info(f"Image saved: {img_path}")
        
        if title and content:
            try:
                author = c.userobj.name if c.userobj else 'Anonymous'
                blog_post = BlogPost(
                    title=title,
                    content=content,
                    author=author,
                    thumbnail=thumbnail_path,
                    images=json.dumps(images_paths) if images_paths else None
                )
                model.Session.add(blog_post)
                model.Session.commit()
                h.flash_success(_('Blog post created successfully!'))
                return redirect(url_for('blog.read', id=blog_post.id))
            except Exception as e:
                model.Session.rollback()
                h.flash_error(_('Error creating blog post: %s') % str(e))
        else:
            h.flash_error(_('Please fill in all fields'))
    
    return render_template('blog/form.html')

@blog_blueprint.route('/blog/<id>', endpoint='read')
def read(id):
    """Membaca post blog tertentu"""
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user,
        'auth_user_obj': c.userobj
    }
    
    try:
        blog_post = model.Session.query(BlogPost).filter(BlogPost.id == id).first()
        if blog_post:
            post = blog_post.to_dict()
            return render_template('blog/read.html', post=post)
        else:
            h.flash_error(_('Blog post not found'))
            return render_template('blog/read.html', post=None)
    except Exception as e:
        h.flash_error(_('Error loading blog post: %s') % str(e))
        return render_template('blog/read.html', post=None)

@blog_blueprint.route('/blog/<id>/edit', methods=['GET', 'POST'], endpoint='edit')
def edit(id):
    """Form untuk mengedit post blog"""
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user,
        'auth_user_obj': c.userobj
    }
    
    try:
        check_access('sysadmin', context)
    except NotAuthorized:
        h.flash_error(_('Not authorized to edit blog posts'))
        return redirect(url_for('blog.index'))
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')
        
        try:
            blog_post = model.Session.query(BlogPost).filter(BlogPost.id == id).first()
            if not blog_post:
                h.flash_error(_('Blog post not found'))
                return redirect(url_for('blog.index'))
            
            blog_post.title = title
            blog_post.content = content
            
            if 'thumbnail' in request.files:
                thumbnail_file = request.files['thumbnail']
                if thumbnail_file and thumbnail_file.filename:
                    thumbnail_path = save_uploaded_file(thumbnail_file, 'thumb')
                    blog_post.thumbnail = thumbnail_path
            
            images_paths = []
            if 'images' in request.files:
                image_files = request.files.getlist('images')
                for image_file in image_files:
                    if image_file and image_file.filename:
                        img_path = save_uploaded_file(image_file, 'img')
                        if img_path:
                            images_paths.append(img_path)
            
            if images_paths:
                existing_images = []
                if blog_post.images:
                    try:
                        existing_images = json.loads(blog_post.images)
                    except:
                        existing_images = []
                existing_images.extend(images_paths)
                blog_post.images = json.dumps(existing_images) if existing_images else None
            
            if title and content:
                model.Session.commit()
                h.flash_success(_('Blog post updated successfully!'))
                return redirect(url_for('blog.read', id=id))
            else:
                h.flash_error(_('Please fill in all fields'))
        except Exception as e:
            model.Session.rollback()
            h.flash_error(_('Error updating blog post: %s') % str(e))
    
    try:
        blog_post = model.Session.query(BlogPost).filter(BlogPost.id == id).first()
        if blog_post:
            post = blog_post.to_dict()
        else:
            h.flash_error(_('Blog post not found'))
            return redirect(url_for('blog.index'))
    except Exception as e:
        h.flash_error(_('Error loading blog post: %s') % str(e))
        return redirect(url_for('blog.index'))
    
    return render_template('blog/form.html', post=post)

@blog_blueprint.route('/blog/<id>/delete', methods=['GET', 'POST'], endpoint='delete')
def delete(id):
    """Menghapus post blog"""
    context = {
        'model': model,
        'session': model.Session,
        'user': c.user,
        'auth_user_obj': c.userobj
    }
    
    try:
        check_access('sysadmin', context)
    except NotAuthorized:
        h.flash_error(_('Not authorized to delete blog posts'))
        return redirect(url_for('blog.index'))
    
    if request.method == 'POST':
        try:
            blog_post = model.Session.query(BlogPost).filter(BlogPost.id == id).first()
            if blog_post:
                model.Session.delete(blog_post)
                model.Session.commit()
                h.flash_success(_('Blog post deleted successfully!'))
            else:
                h.flash_error(_('Blog post not found'))
        except Exception as e:
            model.Session.rollback()
            h.flash_error(_('Error deleting blog post: %s') % str(e))
        
        return redirect(url_for('blog.index'))
    
    try:
        blog_post = model.Session.query(BlogPost).filter(BlogPost.id == id).first()
        if blog_post:
            post = blog_post.to_dict()
        else:
            h.flash_error(_('Blog post not found'))
            return redirect(url_for('blog.index'))
    except Exception as e:
        h.flash_error(_('Error loading blog post: %s') % str(e))
        return redirect(url_for('blog.index'))
    
    return render_template('blog/delete.html', post=post)

