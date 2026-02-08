import html2text
import os
import re
from .template_environment import TemplateEnvironment
from .utils import clean_path, parse_checkin_file, to_datetime

from beer_log.beer import Database
import rss_py

# TODO: Cleanup global variables and include in the BeerLog class.
# db, root, and template_enviornment can all be created within BeerLog.

# TODO: Create a add_checkin() function to create new beer checkins.

# TODO: Allow users to enable/disable RSS generation.

root = os.path.dirname(os.path.abspath(__file__))
template_environment = None

db = Database(os.path.join(os.getcwd(), "beer.db"))

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.bypass_tables = True
text_maker.ignore_images = True


class BeerLog():

    def __init__(
            self,
            content_dir="content/beer",
            templates_dir=os.path.join(root, "templates"),
            output_dir=os.path.join(os.getcwd(), "beer"),
            prefix=None,
            base_url=None,
            ):

        self.output_dir = clean_path(output_dir)

        self.template_environment = TemplateEnvironment(templates_dir)

        self.prefix = prefix
        if prefix is None:
            self.prefix = ""

        self.base_url = base_url
        if base_url is None:
            self.base_url="http://localhost:8000/"

        if not os.path.exists(content_dir):
            print(f"Content path {os.path.abspath(content_dir)} does not exist")
            return False
        self.content_dir = content_dir

    def process_checkins(self):
        for filename in os.listdir(self.content_dir):
            if filename.endswith(".md") and filename != "index.md":
                file_path = os.path.join(self.content_dir, filename)
                checkin_data = parse_checkin_file(file_path)
                checkin_id = os.path.splitext(filename)[0]

                if not all(
                    [checkin_data['beer_name'],
                     checkin_data['brewery_name'],
                     checkin_data['timestamp']]
                        ):
                    print(f"Skipping {filename} due to missing data.")
                    continue

                brewery_id = db.create_brewery_if_not_exists(
                    checkin_data["brewery_name"]
                )

                beer_id = db.create_beer_if_not_exists(
                    checkin_data["beer_name"],
                    brewery_id
                )

                db.create_checkin(
                    checkin_id, beer_id,
                    checkin_data['rating_score'],
                    checkin_data['timestamp'],
                    checkin_data['description'],
                    checkin_data['image']
                )
        self.render_checkins()
        self.render_beers()
        self.render_breweries()

    def render_pages(
            self, template_page,
            folder_name, page_name='index.html',
            **kwargs):
        # TODO: Better default pages.
        # Default pages are currently just stripped from my custom template
        # without CSS. Create better defaults that work with HTML elements
        # and none or minimal styles.

        template = self.template_environment.env.get_template(template_page)
        filename = os.path.join(folder_name, page_name)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as fh:
            fh.write(template.render(
                **kwargs, prefix=self.prefix
            ))

    def render_breweries(self):
        # /beer/<brewery/ shows all beers checked-in from a brewery
        breweries = db.get_breweries()
        for brewery_row in breweries:
            brewery_dict = dict(brewery_row)
            brewery_dict['slug'] = re.sub(r'\W+', '-', brewery_dict['name']).strip('-').lower()

            brewery_beers = db.get_beers_for_brewery(brewery_dict['id'])

            brewery_beers_with_slugs = []
            for beer_row in brewery_beers:
                beer_dict = dict(beer_row)
                beer_dict['slug'] = re.sub(r'\W+', '-', beer_dict['name']).strip('-').lower()
                brewery_beers_with_slugs.append(beer_dict)

            self.render_pages(
                'brewery_page.html',
                os.path.join(self.output_dir, brewery_dict['slug']),
                'index.html',
                brewery=brewery_dict,
                beers=brewery_beers_with_slugs
            )

    def render_beers(self):
        # /beer/<brewery>/<beer>/ shows all checkins for a beer
        beers = db.get_beers()
        for beer_row in beers:
            beer_dict = dict(beer_row)
            brewery = db.get_brewery(beer_dict['brewery_id'])
            brewery_dict = dict(brewery)
            brewery_dict['slug'] = re.sub(r'\W+', '-', brewery_dict['name']).strip('-').lower()

            beer_checkins = db.get_checkins_for_beer(beer_dict['id'])

            beer_dict['slug'] = re.sub(r'\W+', '-', beer_dict['name']).strip('-').lower()

            latest_checkin = None
            if beer_checkins:
                latest_checkin = beer_checkins[0]

            self.render_pages(
                'beer_page.html',
                os.path.join(
                    self.output_dir, brewery_dict['slug'],
                    beer_dict['slug']
                ),
                'index.html',
                beer=beer_dict,
                brewery=brewery_dict,
                checkins=beer_checkins,
                latest_checkin=latest_checkin
            )

    def render_checkins(self):
        checkins = db.get_checkins()
        print(self.output_dir)
        # /beer/ page with all check-ins
        checkins_with_slugs = []
        rss_items = []
        for checkin in checkins:
            checkin_dict = dict(checkin)
            checkin_dict['beer_slug'] = re.sub(r'\W+', '-', checkin['beer_name']).strip('-').lower()
            checkin_dict['brewery_slug'] = re.sub(r'\W+', '-', checkin['brewery_name']).strip('-').lower()
            checkin_dict['slug'] = f"{checkin_dict['brewery_slug']}/{checkin_dict['beer_slug']}/{checkin_dict['checkin_id']}"
            checkins_with_slugs.append(checkin_dict)
            self.render_pages(
                'checkin_page.html',
                os.path.join(
                    self.output_dir,
                    str(checkin_dict['brewery_slug']),
                    str(checkin_dict['beer_slug']),
                    str(checkin['checkin_id'])
                ),
                'index.html',
                checkin=checkin_dict
            )
            rss_items.append(rss_py.Item(
                title=f"{checkin_dict['brewery_name']} - {checkin_dict['beer_name']}",
                pubDate=to_datetime(checkin_dict['timestamp']),
                link=f"{self.base_url}{checkin_dict['slug']}"
            ))
        self.render_pages(
            'beer.html', self.output_dir,
            'index.html', checkins=checkins_with_slugs
        )

        feed = rss_py.Channel(
            title="My beer log",
            description="Recent beer I've drunk.",
            link=self.base_url,
            items=rss_items
        )
        rss_feed = rss_py.build(feed)
        with open(
            os.path.join(self.output_dir, "index.xml"),
            'w') as fh:
            fh.write(rss_feed)

        return True
