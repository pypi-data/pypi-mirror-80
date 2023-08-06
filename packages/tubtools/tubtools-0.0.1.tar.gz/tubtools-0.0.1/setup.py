from setuptools import setup, find_packages

setup(name='tubtools',
      description='Scraping tools for the TU Berlin web portals',
      url='https://gitlab.tubit.tu-berlin.de/bongo0594/tubtools',
      author='Sebastian Bräuer',
      author_email='braeuer@tu-berlin.de',
      license='MIT',
      zip_safe=False,
      install_requires=[
            'fleep',
            'requests',
            'beautifulsoup4'
      ],
      python_requires='>=3.6',
      packages=find_packages(),
      classifiers=[
            "Programming Language :: Python :: 3",
            'Development Status :: 3 - Alpha',
            "License :: OSI Approved :: MIT License",
      ],
      entry_points={
            'console_scripts': [
                  'isisdl = tubtools.isis:main',
                  'moses-export = tubtools.moses:main'
            ]
      })
