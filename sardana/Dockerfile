FROM mambaorg/micromamba:0.25.1-jammy
ENV PYTHONUNBUFFERED 1

RUN micromamba install --name base --channel conda-forge python=3.10.6 sardana=3.3.5
#RUN conda install --channel conda-forge python=3.9.13 sardana=3.2.1

COPY start.py /
CMD [ "/start.py" ]
#CMD [ "/opt/conda/bin/Sardana", "area51" ]
