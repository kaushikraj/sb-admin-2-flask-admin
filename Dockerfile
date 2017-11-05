FROM python:3.6.1


# = OS dependencies
#   - Should not change often
RUN echo "* Installing OS resources" \
  && apt update \
  && apt -y install \
    nodejs \
    npm \
  && echo "* Cleaning OS cache" \
  && rm -rf /varlib/apt \
  && echo "* HACKING for nodejs on Debian" \
  && update-alternatives --install /usr/bin/node node /usr/bin/nodejs 9\
  && echo "* Installing JS dependencies" \
  && npm install -g bower


# = App relative layers
#
WORKDIR /app

# == Python code
COPY ./requirements.txt ./requirements.txt
RUN echo "* Installing project dependencies" \
  && pip install --upgrade pip \
  && pip install -r requirements.txt

# == JS code
COPY ./bower.json ./bower.json
RUN echo "* Installing js assets dependencies" \
  && bower install --allow-root ./bower.json


# = Runtime
#
EXPOSE "5000"
CMD ["python", "app.py"]

# == Add the python code finally
COPY ./ ./
