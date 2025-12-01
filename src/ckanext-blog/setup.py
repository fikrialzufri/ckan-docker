from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='ckanext-blog',
    version=version,
    description="CKAN extension untuk fitur blog",
    long_description="""Extension CKAN untuk menambahkan fitur blog/post ke CKAN instance.""",
    classifiers=[],
    keywords='',
    author='CKAN',
    author_email='info@ckan.org',
    url='',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points='''
        [ckan.plugins]
        blog=ckanext.blog.plugin:BlogPlugin
    ''',
)

