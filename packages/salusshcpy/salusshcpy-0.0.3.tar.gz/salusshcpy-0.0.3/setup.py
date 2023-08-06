from setuptools import find_packages, setup

setup(
    name="salusshcpy",
    version="0.0.3",
    author="Emre Bolat",
    author_email="emre-bolat@hotmail.de",
    description="Salus Smart Home Controller API Python Library",
    license='bsd-3-clause',
    packages=["salusshcpy"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: BSD License"
    ],
    platform='any',
    python_requires='>=3.7',
    install_requires=['requests>=2.22']
)