from setuptools import setup, find_packages

setup(name='streamhub',
      version='0.2.17',
      url='https://bitbucket.org/fivecool/streamhub-singer',
      license='MIT',
      author='Streamhub',
      author_email='tony@streamhub.co.uk',
      description='Streamhub helper lib to make it easier to write Singer target for Streamhub Activate',
      packages=find_packages(),
      long_description='This is a library to facilitate the creation of Singer taps and targets for the Streamhub platform.',
      zip_safe=False,
      python_requires='>=3.6',
      install_requires=[
          'boto3>=1.10.8',
          'botocore>=1.13.8',
          'singer-python==5.9.0',
          'jsonschema==2.6.0'
      ]
      )
