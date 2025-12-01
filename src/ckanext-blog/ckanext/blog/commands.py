import click
import ckan.model as model
from ckanext.blog.model import BlogPost, Base


@click.group()
def blog():
    """Blog commands."""
    pass


@blog.command()
@click.pass_context
def init_db(ctx):
    """Initialize blog database tables."""
    Base.metadata.create_all(model.meta.engine)
    click.echo('Blog database tables initialized.')


def get_commands():
    return [blog]

