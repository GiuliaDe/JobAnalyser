import os
from processhtml import *
from tagcloud import *
from collections import Counter
from tagme import *
import pprint



entities = []

for filename in os.listdir(PAGES_DIR):
    text = html_to_text(os.path.join(PAGES_DIR, filename))
    if text:
        text_entities = get_entities(query_tagme(text), 0.2)
        print text_entities
        entities += text_entities

c = Counter(entities)
print c.most_common(100)
generate_tag_cloud(c.most_common(100), "corriere_entity.png")