FROM python:slim

RUN set -x \
  && apt-get update \
  && apt-get upgrade -y \
  && rm -rf /var/lib/apt/lists/* \
  \
  && pip install --no-cache-dir \
    scrapegraphai \
    scrapegraphai[burr] \
    asyncio \
    uvicorn \
    mcp \
  \
  && playwright install-deps \
  && playwright install

COPY server.py /
ENTRYPOINT ["python", "/server.py"]