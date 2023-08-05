from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='sp_yt_search',
    packages=['sp_yt_search'],
    version='0.0.3',
    license='MIT',
    description='',
    author='Marcin Myśliwiec',
    author_email='marcin.mysliw@gmail.com',
    url='https://github.com/MarcinMysliwiec/sp_yt_searcher',
    download_url='https://github.com/MarcinMysliwiec/sp_yt_searcher/blob/master/dist/sp_yt_search-0.0.3.tar.gz',
    keywords=['first', 'sp_yt_search'],
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your
        # mysliwim_first_pypi
        'Intended Audience :: Developers',
        # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
