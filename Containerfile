FROM python:slim

RUN set -x \
  && apt update \
  && apt upgrade -y \
  && apt install -y \
    tini \
  \
  && pip install --no-cache-dir \
    scrapegraphai \
    scrapegraphai[burr] \
    asyncio \
    uvicorn \
    mcp \
  \
  && playwright install-deps \
  && playwright install \
  && rm -rf /var/lib/apt/lists/* \

ENTRYPOINT ["tini", "--"]