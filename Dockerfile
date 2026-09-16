# ---------------------------------------------------------------------------
#  Image pédagogique 4G/5G — OMNeT++ 6.1.0 + INET 4.5.4 + Simu5G 1.3.0
#  Mode headless (Cmdenv) + JupyterLab pour l'analyse des résultats.
#  Build :  docker build -t tp5g:2026 .          (≈ 30-45 min, ~4 Go)
# ---------------------------------------------------------------------------
FROM ubuntu:22.04

ARG OMNETPP_VERSION=6.1.0
ARG INET_VERSION=4.5.4
ARG SIMU5G_VERSION=1.3.0
ENV DEBIAN_FRONTEND=noninteractive TZ=Europe/Paris

# --- Dépendances système -------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential pkg-config ccache clang lld gdb bison flex perl \
      python3 python3-pip python3-venv libpython3-dev \
      libxml2-dev zlib1g-dev libdw-dev \
      wget curl ca-certificates git nano less xz-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir "numpy<2" "pandas<3" "matplotlib<4" "scipy<2" \
      seaborn jupyterlab ipywidgets posix_ipc

WORKDIR /opt

# --- OMNeT++ (sans IDE, sans Qtenv/OSG : version headless) --------------
RUN wget -q https://github.com/omnetpp/omnetpp/releases/download/omnetpp-${OMNETPP_VERSION}/omnetpp-${OMNETPP_VERSION}-linux-x86_64.tgz \
    && tar xzf omnetpp-${OMNETPP_VERSION}-linux-x86_64.tgz \
    && rm omnetpp-${OMNETPP_VERSION}-linux-x86_64.tgz \
    && mv omnetpp-6.1* omnetpp
ENV OMNETPP_ROOT=/opt/omnetpp
ENV PATH=${OMNETPP_ROOT}/bin:${PATH}
SHELL ["/bin/bash", "-c"]
RUN cd omnetpp \
    && rm -rf ide doc samples \
    && source ./setenv -q \
    && ./configure WITH_QTENV=no WITH_OSG=no WITH_OSGEARTH=no \
    && make -j"$(nproc)" MODE=release

# --- INET Framework ------------------------------------------------------
RUN wget -q https://github.com/inet-framework/inet/releases/download/v${INET_VERSION}/inet-${INET_VERSION}-src.tgz \
    && tar xzf inet-${INET_VERSION}-src.tgz && rm inet-${INET_VERSION}-src.tgz \
    && mv inet4.5* inet
ENV INET_ROOT=/opt/inet
RUN cd inet && source ./setenv && make makefiles && make -j"$(nproc)" MODE=release

# --- Simu5G ---------------------------------------------------------------
RUN wget -q -O simu5g.tgz https://github.com/Unipisa/Simu5G/archive/refs/tags/v${SIMU5G_VERSION}.tar.gz \
    && tar xzf simu5g.tgz && rm simu5g.tgz && mv Simu5G-${SIMU5G_VERSION} simu5g
ENV SIMU5G_ROOT=/opt/simu5g
RUN cd simu5g && source ${INET_ROOT}/setenv && source ./setenv -f \
    && make makefiles && make -j"$(nproc)" MODE=release

# --- Environnement d'exécution -------------------------------------------
ENV PATH=${SIMU5G_ROOT}/bin:${INET_ROOT}/bin:${PATH}
ENV LD_LIBRARY_PATH=${SIMU5G_ROOT}/src:${INET_ROOT}/src:${OMNETPP_ROOT}/lib
ENV OMNETPP_IMAGE_PATH=${OMNETPP_ROOT}/images:${INET_ROOT}/images:${SIMU5G_ROOT}/images

COPY scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/*

# Test de fumée au build : la simu tutorial LTE doit tourner 1 s
RUN cd ${SIMU5G_ROOT}/simulations/LTE/tutorial \
    && simu5g -u Cmdenv -c SingleCell-DL -r 0 --sim-time-limit=1s > /dev/null \
    && rm -rf results

WORKDIR /tp
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]    && make -j"$(nproc)" MODE=release \
    && rm -rf ide doc samples

# --- INET Framework ------------------------------------------------------
RUN wget -q https://github.com/inet-framework/inet/releases/download/v${INET_VERSION}/inet-${INET_VERSION}-src.tgz \
    && tar xzf inet-${INET_VERSION}-src.tgz && rm inet-${INET_VERSION}-src.tgz \
    && mv inet4.5* inet
ENV INET_ROOT=/opt/inet
RUN cd inet && source ./setenv && make makefiles && make -j"$(nproc)" MODE=release

# --- Simu5G ---------------------------------------------------------------
RUN wget -q -O simu5g.tgz https://github.com/Unipisa/Simu5G/archive/refs/tags/v${SIMU5G_VERSION}.tar.gz \
    && tar xzf simu5g.tgz && rm simu5g.tgz && mv Simu5G-${SIMU5G_VERSION} simu5g
ENV SIMU5G_ROOT=/opt/simu5g
RUN cd simu5g && source ${INET_ROOT}/setenv && source ./setenv -f \
    && make makefiles && make -j"$(nproc)" MODE=release

# --- Environnement d'exécution -------------------------------------------
ENV PATH=${SIMU5G_ROOT}/bin:${INET_ROOT}/bin:${PATH}
ENV LD_LIBRARY_PATH=${SIMU5G_ROOT}/src:${INET_ROOT}/src:${OMNETPP_ROOT}/lib
ENV OMNETPP_IMAGE_PATH=${OMNETPP_ROOT}/images:${INET_ROOT}/images:${SIMU5G_ROOT}/images

COPY scripts/ /usr/local/bin/
RUN chmod +x /usr/local/bin/*

# Test de fumée au build : la simu tutorial LTE doit tourner 1 s
RUN cd ${SIMU5G_ROOT}/simulations/LTE/tutorial \
    && simu5g -u Cmdenv -c SingleCell-DL -r 0 --sim-time-limit=1s > /dev/null \
    && rm -rf results

WORKDIR /tp
EXPOSE 8888
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", \
     "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
