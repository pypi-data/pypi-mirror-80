from setuptools import setup

setup(
    name='glossika',
    version='1.0',
    description='Draw pitch for your audio file',
    author='Peter',
    author_email='peter_wang@glossika.com',
    install_requires=["pydub", "parselmouth","numpy","seaborn"],
    license='MIT',
    packages=['speech'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
