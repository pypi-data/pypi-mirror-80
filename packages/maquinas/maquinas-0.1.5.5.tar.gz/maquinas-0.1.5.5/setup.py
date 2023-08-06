from distutils.core import setup
setup(
  name = 'maquinas',
  packages = ['maquinas','maquinas.regular','maquinas.contextfree','maquinas.parser','maquinas.contextsensitive','maquinas.recursivelyenumerable'],
  version = '0.1.5.5',
  license='GNU General Public License v3 or later',
  description = 'Formal languages and automata library',
  author = 'Ivan Vladimir Meza Ruiz',
  author_email = 'ivanvladimir+maquinas@domain.com',
  url = 'https://gitlab.com/ivanvladimir/maquinas',
  download_url = 'https://gitlab.com/ivanvladimir/maquinas/-/archive/v0.1.5.5/maquinas-v0.1.5.5.zip',
  keywords = ['regular languages', 'contect free languages', 'context sensitive languages', 'recursively enumerable languages'],
  install_requires=[
          'graphviz',
          'IPython',
	  'ordered_set',
          'Pillow',
          'TatSu'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Education',
    'Topic :: Education',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
  ],
)
