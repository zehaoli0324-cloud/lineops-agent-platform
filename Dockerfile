FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY lineops ./lineops
RUN pip install --no-cache-dir '.[mqtt]'
ENV LINEOPS_DB=/data/lineops.sqlite
RUN mkdir /data
EXPOSE 8000
CMD ["lineops", "serve", "--host", "0.0.0.0"]
