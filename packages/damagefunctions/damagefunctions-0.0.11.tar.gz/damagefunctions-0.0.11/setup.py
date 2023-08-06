import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

project_urls = {
  'GitHub': 'https://github.com/Pranavesh-Panakkal/damagefunctions'
}

setuptools.setup(
    name="damagefunctions", # Replace with your own username
    version="0.0.11",
    author="Pranavesh Panakkal",
    author_email="ppranavesh@gmail.com",
    description="Flood residential damage functions",
    keywords = ['residential', 'damage functions'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pranavesh-Panakkal/damagefunctions",
    # download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
    packages=setuptools.find_packages(include=["damagefunctions"]),
    classifiers=[
        'Development Status :: 3 - Alpha', # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = project_urls,
    python_requires='>=3.6',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)