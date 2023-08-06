import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

# noinspection SpellCheckingInspection
setuptools.setup(
    name='hellpy',
    license='MIT',
    version='1.1.0',
    python_requires=">=3.6",
    author='Manan (mentix02)',
    long_description=long_description,
    description='A connector for HellDB.',
    author_email='manan.yadav02@gmail.com',
    packages=['hellpy', 'hellpy.structures'],
    url='https://github.com/helldatabase/hellpy',
    long_description_content_type='text/markdown',
    classifiers=[
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
