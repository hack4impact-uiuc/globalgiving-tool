from setuptools import setup

setup(
    name="click-global-giving-tool",
    version="1.0",
    packages=["globalgiving", "globalgiving.commands"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        globalgiving=globalgiving.cli:cli
    """,
)