import setuptools

with open("quicksom/README.md", "r") as fh:
    long_description = fh.read()

requirements = ["numpy>1.0",
                "scipy>0.1",
                "scikit_image>0.15",
                "scikit_learn>0.22"]


setuptools.setup(
    name="quicksom",
    version="0.0.4",
    author="Vincent Mallet and Guillaume Bouvier",
    author_email="vincent.mallet96@gmail.com",
    description="Self Organizing Maps efficient implementation using PyTorch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bougui505/quicksom",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    scripts=['quicksom/bin/quicksom_fit',
             'quicksom/bin/quicksom_gui',
             'quicksom/bin/quicksom_predict',
             'quicksom/bin/quicksom_extract',
             'quicksom/bin/quicksom_project',
             'quicksom/bin/quicksom_flow',
             'quicksom/bin/mdx',
             'quicksom/bin/dcd2npy']
)
