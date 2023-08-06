from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

#with open('HISTORY.md') as history_file:
#    HISTORY = history_file.read()

setup_args = dict(
    name='labelizer',
    version='0.0.0b1',
    description='Protein analysis toolbox for fluorescent labelling and FRET assays',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Christian Gebhardt',
    author_email='christian.gebhardt@bio.lmu.de',
    keywords=['fluorescent label analysis', 'FRET assay'],
    url='https://github.com/ChristianGebhardt/labelizer',
    download_url='https://pypi.org/project/labelizer/'
)

python_requires='>=3.7,<3.8'

install_requires = [
    'biopython>=1.74',
]
#    'cmake>=3.17',
#    'LabelLib=2019.10.9',

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
