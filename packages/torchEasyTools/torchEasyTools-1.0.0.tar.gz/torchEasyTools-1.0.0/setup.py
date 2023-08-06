import setuptools

setuptools.setup(
    name="torchEasyTools",
    version="1.0.0",
    author="samonsix",
    author_email="samonsix@163.com",
    description="easy to load pretrain model and compute model complexity",
    url="https://github.com/Samonsix",
    packages=setuptools.find_packages(),
    install_requires=["torchvision>=0.2.1", "torch>=1.0.0", "numpy>=1.19.0"],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.onnx', '*.jpg'],
    },
    keywords=('torch profile', 'torch pretraind', 'torch model complexity'),
    include_package_data=True,
)
