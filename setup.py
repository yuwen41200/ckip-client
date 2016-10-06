from setuptools import setup


def readme():
    with open('README.rst') as fd:
        return fd.read()

setup(
    name='ckip-client',
    version='0.1.0',
    description='A Python Client for CKIP Chinese Word Segmentation System',
    long_description=readme(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='chinese word segmentation ckip client nlp linguistics',
    url='https://github.com/yuwen41200/ckip-client',
    author='Yu-wen Pwu',
    author_email='ywpu@cs.nctu.edu.tw',
    license='MIT',
    packages=['ckipclient'],
    include_package_data=True,
    zip_safe=False
)
