from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='futils-grab',
    version='0.0.3',
    description='Project renamed, install folkol.grab instead.',
    url='https://github.com/folkol/grab',
    author='folkol',
    classifiers=[
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Filters',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='shell, unix filter',
    install_requires=['folkol.grab'],
    python_requires='>=3.6, <4',
)
