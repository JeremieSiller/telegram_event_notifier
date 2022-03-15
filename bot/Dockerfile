FROM python

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m pip install --upgrade pip
WORKDIR /project

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .

# Run the application:
CMD ["python", "./run.py"]