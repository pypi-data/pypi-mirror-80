
from distutils.core import setup
setup(
  name = 'FastInductiveGraphRepresentationLearning',         
  packages = ['FastInductiveGraphRepresentationLearning'],   
  version = '0.1',      
  license='MIT',        
  description = 'python implementation of the fast inductive graph representation learning algotithm',   
  author = 'HENDRIK TYTGAT',                   
  author_email = 'hjrtytgat@gmail.com',      
  url = 'https://github.com/HendrikTytgat/FastInductiveGraphRepresentationLearning',   
  download_url = 'https://github.com/HendrikTytgat/FastInductiveGraphRepresentationLearning/archive/0.1.tar.gz',    
  keywords = ['Graph', 'Embeddings', 'Inductive'],  
  install_requires=[           
          'numpy',
          'networkx',
          'pandas',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
