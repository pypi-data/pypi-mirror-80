import setuptools

setuptools.setup(
    name="helmer",
    version="0.0.2",
    install_requires=["pyyaml"],
    description="Very basic package manager for helm k8s package manager",
    author="Roman Dolgyi",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["helmer=helmer.helmer:main",],},
)
