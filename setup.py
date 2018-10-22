from setuptools import setup

setup(
    name="click-global-giving-tool",
    version="1.0",
    packages=["gg", "gg.commands"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        gg=gg.cli:cli
    """,
)
