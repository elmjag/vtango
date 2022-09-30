FROM continuumio/miniconda3:4.9.2

RUN conda install --channel conda-forge pytango=9.3.3 flask=2.0.1

COPY cats.py index.py /
CMD ["/index.py"]
