import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='zhangbin_test1',
    version='0.0.2',
    author='zhangbin',
    author_email='zbaa112233@qq.com',
    description='just my testing file to add someday',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stevenbin/zhangbin',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)