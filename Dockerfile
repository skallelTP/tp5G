# ---------------------------------------------------------------------------
#  Image pédagogique 4G/5G — construite avec opp_env, l'installateur OFFICIEL
#  d'OMNeT++ : il télécharge et compile OMNeT++ + INET + Simu5G 1.3.0 avec les
#  versions et options testées par l'équipe OMNeT++ (recette maintenue par eux).
#  Ajouts : JupyterLab + pandas/matplotlib, scripts tp-*.
# ---------------------------------------------------------------------------
FROM ghcr.io/omnetpp/opp_env:latest

USER opp_env
ENV HOME=/home/opp_env
WORKDIR /home/opp_env/default_workspace

# Simu5G 1.3.0 et ses dépendances (OMNeT++, INET) — release uniquement, avec test de fumée
RUN bash -c 'source ~/.venv/bin/activate \
    && source ~/.nix-profile/etc/profile.d/nix.sh \
    && cd ~/default_workspace \
    && opp_env install simu5g-1.3.0 --no-pause --build-modes release --smoke-test'

# Outils d'analyse Python (dans le venv de opp_env)
RUN bash -c 'source ~/.venv/bin/activate \
    && uv pip install "numpy<2" "pandas<3" "matplotlib<4" scipy seaborn jupyterlab ipywidgets'

# Scripts des TP (tp-run, tp-export, tp-export-vec, tp-shell) — ~/bin est dans le PATH
COPY --chown=opp_env:root scripts/ /home/opp_env/bin/
RUN chmod +x /home/opp_env/bin/*

EXPOSE 8888
# On n'utilise pas l'entrypoint interactif de l'image de base
ENTRYPOINT []
CMD ["/home/opp_env/bin/tp-jupyter"]
