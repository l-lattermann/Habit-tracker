import setuptools as s

s.setup(
    name='Distutils',
    version='1.0',
    description='Python Distribution Utilities',
    author='Greg Ward',
    author_email='gward@python.net',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=s.find_packages(),
    install_requirements=[
          "questionary",
          "numpy",
          "pandas",
          "pytest",
          "coverage"
    ]

      )
input()
