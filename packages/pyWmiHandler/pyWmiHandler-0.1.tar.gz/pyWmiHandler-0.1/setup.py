from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyWmiHandler',
      version='0.1',
      description='Most common used WMI queries and functions wrapper',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Systems Administration',
          'Topic :: System :: Operating System',
          'Environment :: Win32 (MS Windows)',
          'Operating System :: Microsoft :: Windows',
      ],
      keywords='WMI Windows Management Instrumentation ',
      url='https://github.com/utytlanyjoe/pyWmiHandler',
      author='Dariusz Lewandowski',
      author_email='utytlanyjoe@icloud.com',
      license='MIT',
      packages=['pyWMiHandler'],
      install_requires=[
          'pypiwin32',
          'WMI'
      ],
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
