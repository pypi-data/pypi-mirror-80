from distutils.core import setup

setup(
    name="pyobserver",
    packages=["pyobserver"],
    version="1.1",
    license="MIT",
    description="A small library developed with Python 3.6 that implements Observer pattern using RLock to achieve "
                "thread synchronization",
    author="Hugo Diniz",
    author_email="hhldiniz@gmail.com",
    url="https://github.com/hhldiniz/pyevents",
    download_url="https://github.com/hhldiniz/pyevents/archive/v1.0.tar.gz",
    keywords=["events", "observer", "observable"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ]
)
