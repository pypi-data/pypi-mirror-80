import setuptools


def setup():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="pybashrc",
        version="1.1.0",
        author="Jelmer Neeven",
        author_email="author@example.com",
        description="Register python functions as bash commands",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jneeven/pybashrc",
        packages=setuptools.find_packages(),
        install_requires=["click >= 7.0, < 8.0"],
        package_data={
            "": [
                "templates/.bashrc",
                "templates/.pybashrc_aliases",
                "templates/.pybashrc.py",
                "execute.py",
            ],
        },
        entry_points={
            "console_scripts": [
                "pybash=pybashrc.post_setup:post_setup",
                "pybash-configure=pybashrc.post_setup:post_setup",
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix ",
        ],
        python_requires=">=3.6",
    )


if __name__ == "__main__":
    setup()
