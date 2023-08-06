from distutils.core import setup

setup(
    name='nauschedule',  # How you named your package folder (MyLib)  # Chose the same as "name"
    packages=['nauschedule'],
    version='0.1.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Библиотека для удобной работы с NAU API',  # Give a short description about your library
    author='skiter847',  # Type in your name
    author_email='ivashenco45@gmail.com',  # Type in your E-Mail
    url='https://github.com/skiter847/NauScheduleAPI',  # Provide either the link to your github or to your website
    download_url='https://github.com/skiter847/NauScheduleAPI/archive/0.1.tar.gz',
    keywords=['SCHEDULE', 'API', 'NAU'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'requests',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.9',  # Specify which python versions that you want to support
    ],
)
