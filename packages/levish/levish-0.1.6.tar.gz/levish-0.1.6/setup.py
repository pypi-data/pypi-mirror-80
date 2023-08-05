from distutils.core import setup
setup(
  name = 'levish',
  packages = ['levish'],
  version = '0.1.6',
  license='MIT',
  description = 'Create your own shell.',
  author = 'Aaron Levi Can (aaronlyy)',
  author_email = 'aaronlevican@gmail.com',
  url = 'https://github.com/aaronlyy/levish',
  download_url = 'https://github.com/aaronlyy/levish/archive/v_016.tar.gz',
  keywords = ['shell', 'terminal', 'commands', 'cmd', 'console'],
  install_requires=[
        "pyfiglet"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)