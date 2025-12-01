import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.blog.blueprint import blog_blueprint
from ckanext.blog import commands


class BlogPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.IClick)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')

    def get_blueprint(self):
        return blog_blueprint
    
    def get_commands(self):
        return commands.get_commands()

