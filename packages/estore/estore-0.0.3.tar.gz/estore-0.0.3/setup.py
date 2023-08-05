import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='estore',
    version='0.0.3',
    description='Meta package for estore packages',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lostwire/estore',
    author='Jnxy',
    author_email='jnxy@lostwire.net',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: AsyncIO",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Database" ],
    extras_require = {
        "client": [ "estore-client" ],
        "server": [ "estore-server" ],
        "all": [ "estore-client", "estore-server" ],
    },
    install_requires = [
        'estore-base'
    ])
