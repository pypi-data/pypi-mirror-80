from setuptools import setup, find_packages

setup(name='apetype',
      version='0.0.1',
      description='Embracing builtin python modules argparse and typing',
      url='https://github.com/dicaso/apetype',
      author='Christophe Van Neste',
      author_email='christophe.vanneste@ugent.be',
      license='MIT',
      packages=find_packages(),
      python_requires='>=3.6',
      install_requires=[],
      extras_require={
          'documentation': ['Sphinx']
      },
      package_data={},
      include_package_data=True,
      zip_safe=False,
      entry_points={},
      test_suite='nose.collector',
      tests_require=['nose']
      )

# To install with symlink, so that changes are immediately available:
# pip install -e .
