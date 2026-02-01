import html2text
import os
import markdown
import re
from .template_environment import TemplateEnvironment

from beer_log.beer import Database

root = os.path.dirname(os.path.abspath(__file__))
template_environment = None

db = Database(os.path.join(os.getcwd(), "beer.db"))

content_dir = "content/beer"

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.bypass_tables = True
text_maker.ignore_images = True

def parse_checkin_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(content)
        meta = md.Meta
        
        beer_score
        if meta.get('beer_score') == '':
            beer_score = -1

        checkin_data = {
            'timestamp': meta.get('created_at', [None])[0],
            'rating_score': beer_score,
            'beer_name': meta.get('beer_name', [None])[0],
            'brewery_name': meta.get('brewery_name', [None])[0],
            'description': html,
            'image': meta.get('image', [None])[0]
        }
        return checkin_data

def process_checkins(content_dir=content_dir, templates_dir=os.path.join(root,"templates")):
    global template_environment
    template_environment = TemplateEnvironment(templates_dir)

    if not os.path.exists(content_dir):
        print(f"Content path {os.path.abspath(content_dir)} does not exist")
        return False

    for filename in os.listdir(content_dir):
        if filename.endswith(".md") and filename != "index.md":
            file_path = os.path.join(content_dir, filename)
            checkin_data = parse_checkin_file(file_path)
            checkin_id = os.path.splitext(filename)[0]

            if not all([checkin_data['beer_name'], checkin_data['brewery_name'], checkin_data['timestamp']]):
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

    render_checkins()
    render_beers()
    render_breweries()


def render_pages(template_page, folder_name, page_name='index.html', **kwargs,):
    template = template_environment.env.get_template(template_page)
    filename = os.path.join(root, 'html', folder_name, page_name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fh:
        fh.write(template.render(
            **kwargs
        ))

def render_breweries():
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

        render_pages(
            'brewery_page.html',
            os.path.join(os.getcwd(), 'beer', brewery_dict['slug']),
            'index.html',
            brewery=brewery_dict,
            beers=brewery_beers_with_slugs
        )

def render_beers():
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

        render_pages(
            'beer_page.html',
            os.path.join(
                os.getcwd(), 'beer', brewery_dict['slug'],
                beer_dict['slug']
            ),
            'index.html',
            beer=beer_dict,
            brewery=brewery_dict,
            checkins=beer_checkins,
            latest_checkin=latest_checkin
        )

def render_checkins():
    checkins = db.get_checkins()

    # /beer/ page with all check-ins
    checkins_with_slugs = []
    for checkin in checkins:
        checkin_dict = dict(checkin)
        checkin_dict['beer_slug'] = re.sub(r'\W+', '-', checkin['beer_name']).strip('-').lower()
        checkin_dict['brewery_slug'] = re.sub(r'\W+', '-', checkin['brewery_name']).strip('-').lower()
        checkin_dict['slug'] = f"{checkin_dict['brewery_slug']}/{checkin_dict['beer_slug']}/{checkin_dict['checkin_id']}"
        checkins_with_slugs.append(checkin_dict)
        render_pages(
            'checkin_page.html',
            os.path.join(
                os.getcwd(), 'beer',
                str(checkin_dict['brewery_slug']),
                str(checkin_dict['beer_slug']),
                str(checkin['checkin_id'])
            ),
            'index.html',
            checkin=checkin_dict
        )
    render_pages(
        'beer.html', os.path.join(os.getcwd(), 'beer'),
        'index.html', checkins=checkins_with_slugs
    )

    return True
