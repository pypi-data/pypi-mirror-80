from os.path import join, dirname, abspath

from setuptools import setup, find_packages

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'htmldump',
    version          = '0.2039.0',
    description      = 'HTML Dumper',
    long_description = readme,
    keywords         = ['utility', ],
    url              = 'https://sourceforge.net/p/htmldump/code/ci/stable/tree',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    package_dir = {
        'htmldump': 'htmldump',
    },
    packages = [
        'htmldump',
    ],
    entry_points = dict(
        console_scripts = (
            'html_to_json=htmldump.command:do_html_to_json',
            'html_dump=htmldump.command:do_html_dump',
        ),
    ),
)
