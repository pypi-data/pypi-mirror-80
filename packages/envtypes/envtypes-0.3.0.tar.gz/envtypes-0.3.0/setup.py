import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='envtypes',
    version='0.3.0',
    author='YazeeMe',
    author_email='ionut.badea@yazee.me',
    description="Return the values of the envs with the correct type.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ionut-badea/env-types',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['python-dotenv']
)
