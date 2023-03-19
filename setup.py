from setuptools import setup, find_packages

from pydosa import __version__

setup(
    name='pydosa',
    version=__version__,
    packages=find_packages(),
    scripts=["pydosa/__main__.py", "pydosa/tools/scpi_client.py"],
    include_package_data=True,
    package_data={
        "pydosa.data": ['.pydosa.cfg']
    },
    url='',
    license='MIT License',
    author='Jon Brumfitt',
    author_email='',
    description='Digital Oscilloscope Spectrum Analyzer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        # 'url="https://github.com/jbrumf/pydosa"',
        'License :: OSI Approved :: MIT License'
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research'
    ],
    python_requires='>=3.10',
    install_requires=[
        'python-vxi11>=0.9',
        'numpy',
        'scipy',
        'pytest'
    ]
)
