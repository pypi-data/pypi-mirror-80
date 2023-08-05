import setuptools

setuptools.setup(
    name="grpc-powergate-client",
    version="0.6.0-rc8",
    author="Textile",
    author_email="contact@textile.io",
    url="https://github.com/textileio/powergate",
    packages=setuptools.find_packages(),
    install_requires=[
      'protobuf',
    ],
)
