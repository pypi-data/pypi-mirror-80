from setuptools import setup

with open('py-datastructures/README.md') as f:
    long_description = f.read()

setup(name='py-datastructures',
      version='0.1',
      description='Data Structures using Python',
      packages=['py-datastructures'],
      author = 'Adithya Yelloju',
      author_email = 'adithyayelloju@gmail.com',
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/AdithyaYelloju/Data-Structures-in-Python',
      zip_safe=False)
