from setuptools import setup

module = 'discordmc'
modules = []

setup(
    name=module,
    version='1.1.0',
    packages=[module, *modules],
    license='GNU LIcense',
    author='Pixymon',
    author_email='nlarsen23.student@gmail.com',
    description='Access to your Minecraft Server through discord.',
    install_requires=['discord', 'mcserverapi', 'requests']
)
