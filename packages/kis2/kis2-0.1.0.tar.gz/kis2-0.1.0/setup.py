from setuptools import find_packages, setup


setup(name="kis2",
      version="0.1.0",
      description="Image Segmentation toolkit for keras edited for work",
      author="Gulsima",
      author_email='gulsimabilgin94@gmail.com',
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      license="GPLv3",
      url="https://github.com/rosegit-lab/kis2",
      download_url = 'https://github.com/rosegit-lab/kis2/archive/v_1.tar.gz',
      packages=find_packages(exclude=["test"]),
      entry_points={
            'console_scripts': [
                  'keras_segmentation = keras_segmentation.__main__:main'
            ]
      },
      install_requires=[
            "Keras>=2.0.0",
            "imageio==2.5.0",
            "imgaug==0.2.9",
            "opencv-python",
            "tqdm"],
      extras_require={
            # These requires provide different backends available with Keras
            "tensorflow": ["tensorflow"],
            "cntk": ["cntk"],
            "theano": ["theano"],
            # Default testing with tensorflow
            "tests-default": ["tensorflow", "pytest"]
      }
)