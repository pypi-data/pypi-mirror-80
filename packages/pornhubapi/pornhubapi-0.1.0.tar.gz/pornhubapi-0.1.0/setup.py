from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pornhubapi',
      version='0.1.0',
      description='Pornhub API Wrapper',
      long_description=readme(),
      url='https://github.com/sskender/pornhub-api',
      author='diogenesjunior',
      author_email='diogenesjunior@protonmail.com',
      packages=['pornhub'],
      zip_safe=False,
      keywords='pornhub api',
      license='MIT',
      install_requires=['beautifulsoup4', 'requests', 'lxml'],
      include_package_data=True)
