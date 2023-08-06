from distutils.core import setup
setup(
  name = 'nbjuniper',
  packages = ['nbjuniper'],
  version = '0.1.2',
  license='MIT',
  description = 'Convert Jupyter Notebooks into runnable HTML files with Juniper',
  author = 'Michael Ashton',
  author_email = 'ashtonmv@gmail.com',
  url = 'https://github.com/ashtonmv/nbjuniper',
  download_url = 'https://github.com/ashtonmv/nbjuniper/archive/v_012.tar.gz',
  keywords = ['jupyter', 'website', 'html', 'notebook', 'interactive', 'juniper'],
  install_requires=[ 
          'pyyaml',
          'markdown',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
)