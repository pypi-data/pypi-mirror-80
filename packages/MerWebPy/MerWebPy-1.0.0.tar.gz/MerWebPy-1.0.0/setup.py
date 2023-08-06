from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='MerWebPy',
      version='1.0.0',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url="https://github.com/kessec/MerWebPy",
      author_email="muki@kessec.com",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Operating System :: OS Independent'
      ],
      keywords='merriam webster dictionary query database word noun verb adjective',
      license='MIT',
      packages=['MerWebPy'],
      install_requires=['requests'],
      include_package_data=True)
