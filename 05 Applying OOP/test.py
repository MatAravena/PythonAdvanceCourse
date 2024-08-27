class Relationship():
    def __init__(self, type, from_node, to_node):
        assert isinstance(from_node, Node), 'Relationships need to go from Node to Node'
        assert isinstance(to_node, Node), 'Relationships need to go from Node to Node'
        self.type = type
        self.from_node = from_node
        self.to_node = to_node

class Node():
    def __init__(this, 
                 labels = None,
                 properties = {},
                 relationships = None):
        assert isinstance(relationships, 
                          (type(None),Relationship)), 'relationships must be of class Relationship'
        this.labels = labels
        this.properties = properties
        this.relationships = relationships

    def add_properties(this, property_key, property_value):
        this.properties[property_key] = property_value
        print('{} added.'.format(property_key))

if __name__ == '__main__':
    actor_1 = Node(labels = ['Actor'])
    actor_2 = Node(labels = ['Actor'])
    actor_1.add_properties('name', 'Gary Sinise')
    movie_1 = Node(labels = ['Movie'])
    movie_1.add_properties('title', 'Forrest Gump')
    rel_1 = Relationship('ACTED_IN',
                         from_node = actor_1,
                         to_node = movie_1)

    print(actor_1.relationships)
    print(movie_1.relationships)
    print(actor_1 == actor_2)