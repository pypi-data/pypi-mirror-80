import setuptools
setuptools.setup(name="kssanalysis",
      version="0.3",
      description="This file is responsible to return the context of word",
      author="Kailash, Sudhanshu",
      author_email="kumar.rajiv09876@gmail.com, sudhshreya666@gmail.com",
      url="https://github.com/kailash01/kssanalysis",
      packages=['kssanalysis'],
      data_files=[('POSITIVE.txt') ,('NEGATIVE.txt')],
      install_requires=[])
