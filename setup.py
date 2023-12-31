from distutils.core import setup

setup(
    name="telegraph-export",
    version="1.1",
    description="Exporting urls to telegraph",
    author="Random Person",
    author_email="rand@om.",
    url="https://github.com/Political-deCeit/telegraph-export",
    install_requires=[
        "beautifulsoup4>=4.6.0",
        "readability-lxml",
        "html-telegraph-poster",
        "pillow",
        "requests",
        "telegram_util",
    ],
    packages=["telegraph_export"],
)
