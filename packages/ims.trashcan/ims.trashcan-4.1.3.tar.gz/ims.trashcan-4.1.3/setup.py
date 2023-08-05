from setuptools import setup, find_packages

version = '4.1.3'

setup(name='ims.trashcan',
      version=version,
      description="Stores deleted objects in a trash can before deletion.",
      long_description=open("README.md").read(),
      long_description_content_type='text/markdown',
      classifiers=[
          "Framework :: Plone :: 5.2",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
      ],
      keywords='',
      author='Eric Wohnlich',
      author_email='wohnlice@imsweb.com',
      url='https://github.com/imsweb/ims.trashcan',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ims'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      extras_require={
          'test': ['plone.app.testing', 'plone.mocktestcase', 'formencode'],
      },
      )
