## Setting the project up

Create a virtual environment for python and install packages. Example setup script:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
docker-compose up -d
```

and run a file with:

```
python linkedin/linkedin.py
```

## Accessing Chrome Devtools or debug chrome:

After running the `docker-compose` command to get the container up the UI is available at: `http://localhost:3355/`

More docs and config options can be found here on the browserless.io website - https://docs.browserless.io/
