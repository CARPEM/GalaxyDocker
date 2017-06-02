from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()
        

setup(name='datamanagerpkg',
      version='0.1',
      description='python package to allow communication between Ion Proton and Galaxy',
      long_description=readme(),
      author='William Digan',
      author_email='william.digan@aphp.fr',
      license='MIT',
      packages=['datamanagerpkg'],
      zip_safe=False)
       #~ install_requires=[
          #~ 'markdown',
      #~ ],
            #~ include_package_data=True,
