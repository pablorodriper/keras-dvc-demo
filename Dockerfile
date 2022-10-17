FROM nvcr.io/nvidia/tensorflow:22.09-tf2-py3

# More consistent floating point operations between executions
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV PYTHONHASHSEED=1337

RUN apt update && yes | apt upgrade
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt
# Fix tensorflow incompatibility
RUN pip install protobuf==3.20.0

# Create the user
ARG USERNAME=pablo
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME 
    #
    # # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    # && apt-get update \
    # && apt-get install -y sudo \
    # && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    # && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME