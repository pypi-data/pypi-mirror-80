from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='metrics_computation',
    version='v0.0.2',
    author='Alvaro Mendez Civieta',
    author_email='almendez@est-econ.uc3m.es',
    license='GNU General Public License',
    zip_safe=False,
    url='https://github.com/alvaromc317/metrics_computation',
    description='Given a True beta vector and a predicted beta vector, computes a set of metrics such as true positive rate, recall, etc',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['High dimensional regression', 'metrics', 'true positive rate', 'true negative rate', 'precision', 'recall', 'f-score'],
    python_requires='>=3.5',
    install_requires=["numpy >= 1.15"],
    packages=find_packages()
)
