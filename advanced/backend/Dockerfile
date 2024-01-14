FROM python:3.10

RUN apt-get -y update && apt-get install -y --no-install-recommends build-essential  \
    curl wget nginx ca-certificates \
    && pip install --upgrade pip setuptools \ 
    && rm -rf /var/lib/apt/lists/*

# Set some environment variables. 
# PYTHONUNBUFFERED - keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. 
# PYTHONDONTWRITEBYTECODE - keeps Python from writing the .pyc files which are unnecessary in this case. 
# PATH & PYTHONPATH - We also update PATH &NPYTHONPATH so that the train and serve programs are found when the container is invoked.
ENV PYTHONUNBUFFERED=TRUE PYTHONDONTWRITEBYTECODE=TRUE PATH="/home/user/app:${PATH}" PYTHONPATH="/home/user/app:${PYTHONPATH}"

# Install python libraries
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Add non-root user
RUN groupadd -r user && useradd -r -g user user
RUN chown -R user /var/log/nginx /var/lib/nginx /tmp

# Set up the program in the image
COPY app /home/user/app
WORKDIR /home/user/app

# Chown app folder
RUN chown -R user /home/user/app 

# Expose port
EXPOSE 8080

# Entrypoint
ENTRYPOINT [ "sh", "./entrypoint" ]

# Switch to the user
USER user