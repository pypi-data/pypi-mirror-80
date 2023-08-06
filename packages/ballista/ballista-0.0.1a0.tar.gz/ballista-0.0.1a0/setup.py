import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='ballista',  
     version='v0.0.1-alpha',
     scripts=[] ,
     author="Ceyda Cinarel",
     author_email="snu_ceyda@gmail.com",
     description="Helpers for training with pytorch",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cceyda/Ballista",
     download_url = 'https://github.com/cceyda/Ballista/archive/v0.0.1-alpha.tar.gz',
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    python_requires='>=3.6',
    install_requires=["pyyaml","coloredlogs"]
 )