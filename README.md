# beer-log

Check-in beer when you've drunk some and generate a website to brag about it.

## Installation
```
pip install "git+https://github.com/PeskyPotato/beer-log.git@main"
```

## Getting started

This project is both a Python module and CLI tool that allows you to generate a HTML pages and an RSS feed based on beer you check-in. The tool expects an folder with markdown files each representing a single checkedin beer.

To start create a new markdown file in a folder. In this example the folder will be called `content` and the file will be `2022-08-05-brouwerij-oproer-fizz-pilsner.md`. The file name represents the date of the checkin, the brewery name and beer name. the file name is used for the slug of the URL.

### CLI

To process all the checkins from the `content` directory run the following command.

```bash
beer-log checkin process --content_dir content/
```

This will go through each markdown file in content directory and render the beer checkin if the details in the file are valid. The output by default is saved in a new directory called `beer`. You can change this by passing in the `--output_dir` with a valid, and existing directory on your computer.

To view the files created enter the `beer` directory and create a web server.
```bash
cd beer
python -m http.server
```

Now open http://127.0.0.1:8000/ in you browser to view your checked in beers.

### Python module

To process all the checkins from the `content` directory create a new Pythono file and import the `BeerLog` class.

```python
from beer_log import BeerLog
```

This will be your entry point to the tool. Here we can passe in the location of our content directory and build out HTML files.

```
bl = BeerLog(content_dir="./content")
bl.process_checkins()
```

If you run the file all the checkins from the content directory will be processed with the HTMl generated in the newly created `beer` directory. You can change this default output location by specifying the `output_dir` parameter when creating an instance of `BeerLog`.

Now if you enter the `beer` directory and launch a web server you will be able to view your checked-in beers.

```bash
cd beer
python -m http.server
```

