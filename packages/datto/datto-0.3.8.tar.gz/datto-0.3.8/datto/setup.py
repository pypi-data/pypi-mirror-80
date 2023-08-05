from distutils.core import setup

setup(
setup(name='Datto',
      version='1.0',
      description='Python Distribution Utilities',
      author='Greg Ward',
      author_email='gward@python.net',
      url='https://www.python.org/sigs/distutils-sig/',
    packages=["datto"],
    package_dir={"datto": "datto/datto"},
    package_data={"datto": ["data/*"]},
)

