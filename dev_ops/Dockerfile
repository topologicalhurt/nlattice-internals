FROM topologicalhurt/pymesh-3.10:v1.1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8501

COPY ./Scripts/install_scripts/entry_point.sh /tmp/
COPY ./requirements.txt /tmp/
RUN /bin/bash /tmp/entry_point.sh
