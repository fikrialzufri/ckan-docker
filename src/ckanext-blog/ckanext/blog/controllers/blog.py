import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
from ckan.common import request, c, g, _
import ckan.lib.navl.dictization_functions as dict_fns

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action


class BlogController(base.BaseController):
    
    def index(self):
        """Menampilkan daftar semua post blog"""
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user,
            'auth_user_obj': c.userobj
        }
        
        try:
            # Untuk sekarang, kita akan menggunakan data dummy
            # Nanti bisa diintegrasikan dengan database
            c.posts = [
                {
                    'id': '1',
                    'title': 'Selamat Datang di Blog CKAN',
                    'content': 'Ini adalah post pertama di blog CKAN. Fitur blog memungkinkan Anda untuk berbagi informasi dan update dengan pengguna CKAN.',
                    'author': 'Admin',
                    'created': '2025-12-01'
                }
            ]
            
            return base.render('blog/index.html')
        except Exception as e:
            h.flash_error(_('Error loading blog posts: %s') % str(e))
            return base.render('blog/index.html')
    
    def read(self, id):
        """Membaca post blog tertentu"""
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user,
            'auth_user_obj': c.userobj
        }
        
        try:
            # Dummy data untuk sekarang
            c.post = {
                'id': id,
                'title': 'Contoh Post Blog',
                'content': 'Ini adalah konten dari post blog. Anda dapat menambahkan fitur untuk menyimpan dan mengambil data dari database.',
                'author': 'Admin',
                'created': '2025-12-01'
            }
            
            return base.render('blog/read.html')
        except NotFound:
            base.abort(404, _('Blog post not found'))
    
    def new(self):
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
            base.abort(403, _('Not authorized to create blog posts'))
        
        if request.method == 'POST':
            # Handle form submission
            title = request.params.get('title', '')
            content = request.params.get('content', '')
            
            if title and content:
                h.flash_success(_('Blog post created successfully!'))
                return h.redirect_to('blog_index')
            else:
                h.flash_error(_('Please fill in all fields'))
        
        return base.render('blog/form.html')
    
    def edit(self, id):
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
            base.abort(403, _('Not authorized to edit blog posts'))
        
        if request.method == 'POST':
            title = request.params.get('title', '')
            content = request.params.get('content', '')
            
            if title and content:
                h.flash_success(_('Blog post updated successfully!'))
                return h.redirect_to('blog_read', id=id)
            else:
                h.flash_error(_('Please fill in all fields'))
        
        # Dummy data untuk edit
        c.post = {
            'id': id,
            'title': 'Contoh Post untuk Edit',
            'content': 'Konten yang bisa diedit'
        }
        
        return base.render('blog/form.html')
    
    def delete(self, id):
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
            base.abort(403, _('Not authorized to delete blog posts'))
        
        if request.method == 'POST':
            h.flash_success(_('Blog post deleted successfully!'))
            return h.redirect_to('blog_index')
        
        # Dummy data untuk konfirmasi delete
        c.post = {
            'id': id,
            'title': 'Post yang akan dihapus'
        }
        
        return base.render('blog/delete.html')

