from setuptools import setup
import pypandoc

with open('./README.md', encoding='utf-8') as f:
	long_description = f.read()

# rst_description = pypandoc.convert_text(long_description, 'rst', format='markdown_github')

setup(
	name = "relpath",
	version = '3.0.2',
	description = 'relative path from the python file itself',
	author = 'le latelle',
	author_email = 'g.tiger.ml@gmail.com',
	url = 'https://github.co.jp/',
	packages = ["relpath"],
	install_requires = [],
	long_description = long_description,
	long_description_content_type = "text/markdown",
	license="CC0 v1.0",
	classifiers=[
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries',
		'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
	]
)
