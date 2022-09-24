## Features

```
Lets you crawl and save all the posts of any open linkedin account including its caption, images and other fields
```

## Setting the project up

1. Create a virtual environment for python and install packages. Example setup script:

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

2. Add the .env file to project and  add your linkedin account credentials :
```
USERNAME=ADD_YOUR_USERNAME
PASSWORD=ADD_YOUR_PASSWORD

```
3. Create a folder `Linkedin-Posts` inside `linkedin` folder (if it is not there)


4. and run a file with:

```
cd linkedin
python linkedin.py
```

## To add new open profiles or companies:

To add new companies or profiles whose posts you want to crawl-
 ```
  Add their linkedin profile urls in the array on line 35 in `linkedin/linkedin.py` file
 ```
