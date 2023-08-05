from setuptools import setup

setup(
    name='BtcTurkApi',
    url="https://github.com/uguraltinsoy/BTC-TURK-API",
    version='0.0.4',    
    keywords=['btcturk','btcturkapi', 'bitcoin','api', 'exchange', "btc", "eth", "xrp"],
    install_requires=['requests'],
    description='Python btcturk.com API wrapper.',
    author='Uğur Altınsoy',
    packages=['btcturkapi'],
    modules=['btcturkapi'],
    author_email='ugur.altnsy@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ])
