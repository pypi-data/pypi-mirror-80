import setuptools

with open('requirements.txt', 'r') as fh :
    requirements = fh.read()

with open("README.md", "r") as fh :
    long_description = fh.read()

setuptools.setup(
    name='ds-arpes-plugin',
    version='0.0.2',
    author='Kevin Kramer',
    author_email='kevin.kramer@uzh.ch',
    description='Plugin connecting data_slicer.pit and arpys.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kuadrat/ds_arpes_plugin.git',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
