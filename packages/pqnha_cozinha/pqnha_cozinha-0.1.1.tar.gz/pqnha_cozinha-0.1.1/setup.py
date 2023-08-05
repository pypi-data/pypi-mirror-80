from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
      
setup(name='pqnha_cozinha',
      version="0.1.1",
      description="Início do projeto paçoquinha (aplicativo para a cozinha)",
      long_description=long_description,
      long_description_content_type='ext/markdown',
      url='https://pypi.org/project/pqnha_cozinha/',
      author='(Linux77) Academia do software livre',
      author_email='leonardo@asl-sl.com.br',
      license='MIT',
      classifiers=[
          "License :: OSI Approved :: MIT License",
      ],
      packages=["pq_kitchen"],
      include_pckage_data=True,
      install_requires=["feedparser","html2text"],
      python_requires='>=3.6',
      entry_points={
          "console_scripts":[
              "pq_kitchen = pq_kitchen.__main__:main"
          ]
      },
      
)
