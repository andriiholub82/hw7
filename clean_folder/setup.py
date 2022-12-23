from setuptools import setup

setup(
    name='clean_folder',
    version='1',
    description='Sort folders by file extension',
    url='https://github.com/andriiholub82/hw7.git',
    author='Andrii Holubenko',
    author_email='andrii.holub82@gmail.com',
    license='MIT',
    packages=['clean_folder'],
    include_package_data=True,
    entry_points={'console_scripts': [
        'clean-folder = clean_folder.clean:start_sorting']}
)
