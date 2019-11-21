from neomodel import StructuredNode, IntegerProperty,  \
    StringProperty, DateTimeProperty, FloatProperty, RelationshipTo

class Brawler(StructuredNode):
    url = StringProperty()
    image_url_large = StringProperty()
    image_url_small = StringProperty()
    
    name = StringProperty()
    updated_at = DateTimeProperty()
    
    rank = IntegerProperty()
    
    weight = IntegerProperty()
    air_speed = FloatProperty()
    fall_speed = FloatProperty()
    run_speed = FloatProperty()
    dash_speed = FloatProperty()
    
    universe = StringProperty()
    tier = StringProperty()    
    
    counters = RelationshipTo('Brawler', 'COUNTERS')
    
    def __repr__(self):
        return f"Brawler({self.name})"
