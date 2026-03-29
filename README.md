# beer-log

Check-in beer when you've drunk some and generate a website to brag about it.

## Installation
```
pip install "git+https://github.com/PeskyPotato/beer-log.git@main"
```

## Getting started

This project is both a Python module and CLI tool that allows you to generate HTML pages and an RSS feed based on beer you check-in. The tool expects a folder with markdown files each representing a checked-in beer.

### CLI

To start create a folder called `content` in your current directory. Then using the CLI command to create a new check-in for the beer Superhaas by Terwijde Bierclub with a 4 out of 5 rating.

```bash
beer-log checkin add \
        --brewery "Terwijde Bierclub" \
        --beer "Superhass" \
        --rating 4.0
```

Afer entering the command your default text editor will open up with a partially filled markdown file. You can continue entering more details about your check-in. Once complete save and close the file.

You will now have a new markdown file created inside the content folder. To create a static website from the check-in we will need to process the content directory.

To process all the checkins from the `content` directory run the following command.

```bash
beer-log checkin process --content_dir content/
```

This will go through each markdown file in the directory and render the beer checkin, if the details in the file are valid. The output by default is saved in a new directory called `beer`. You can change this by passing in the `--output_dir` with a valid, and existing directory on your computer.

To view the files created enter the `beer` directory and create a web server.

```bash
cd beer
python -m http.server
```

Now open http://127.0.0.1:8000/ in you browser to view your checked in beers.

### Python module

In order to create a new checkin using the package import the Checkin class and instantiate it. We will be creating a new checkin for the Superhass beer from Terwijde Bierclub with a 4.0 rating.

```python
from beer_log import Checkin

checkin = Checkin(
    beer_name="Superhass",
    brewery_name="Terwijde Bierclub",
    beer_score=4.0,
    content_dir = "./content"
)

checkin.add_checkin()
```

A new markdown file will created in the content directory. You may open this and edit the details of the checkin further.

To process all the checkins from the content directory import the `BeerLog` class.

```python
from beer_log import BeerLog
```

Here you can pass in the location of the content directory and build your HTML files.

```python
bl = BeerLog(content_dir="./content")
bl.process_checkins()
```

If you run the Python file all the checkins from the content directory will be processed with the HTMl generated in the newly created `beer` directory. You can change this default output location by specifying the `output_dir` parameter when creating an instance of `BeerLog`.

Now if you enter the `beer` directory and launch a web server you will be able to view your checked-in beers.

```bash
cd beer
python -m http.server
```
