from distutils.core import setup

setup(
  name = 'downsemble',   
  packages = ['downsemble'],  
  version = '0.0.1',      
  license='MIT',      
  description = 'his classifier is designed to handle imbalanced data. The classification is based on an ensemble of sub-sets.',
  author = 'Roni Gold',                  
  author_email = 'ronigoldsmid@gmail.com', 
  url = 'https://github.com/ronigold',
  download_url = 'https://github.com/ronigold/downsemble/archive/0.0.1.tar.gz',   
  keywords = ['machine learning', 'deep learning', 'model', 'optimizing','imbalanced'],  
  install_requires=[            
          'sklearn',
		  'tqdm',
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
  ],
)