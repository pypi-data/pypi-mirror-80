from business_rules.activate_relationship_frames import ActivateRelationships
from repositories.relationship import RelationshipRepository

ACTION_TYPE_SKIP = 'skip'
ACTION_TYPE_UPDATE = 'update'

# TODO: このファイルは完全に未テスト
class ImportRelationships():
    @property
    def relationship_file_path(self):
        pass

    @relationship_file_path.getter
    def relationship_file_path(self):
        return self.__relationship_file_path

    @property
    def type_in_row(self):
        pass

    @type_in_row.getter
    def type_in_row(self):
        return self.__type_in_row

    @property
    def create_node(self):
        pass

    @create_node.getter
    def create_node(self):
        return self.__create_node

    def __init__(self, file_name, type_in_row = True, create_node = False):
        self.__relationship_file_path = 'importing/%s' % file_name
        self.__type_in_row = type_in_row
        self.__create_node = create_node

        # MEMO: RelationshipRepository でも create_node するかの制御ができるように実装しているけど、
        #       この shell では、ActivateRelationships で制御している。
        self.relationship_repository = RelationshipRepository(self.create_node)

    def invoke(self, action_type = ACTION_TYPE_SKIP):
        # MEMO: ActivateRelationships にて create_node するか決めているけど、 RelationshipRepository にてやる方がいいかも。
        activate_relationships = ActivateRelationships(self.relationship_file_path, self.type_in_row, self.create_node)
        csv_relationships = activate_relationships.invoke()
        
        for relationship in csv_relationships:
            result = self.action(relationship, action_type)
            if not result:
                print('action failed.', relationship, action_type)

    def action(self, relationship, action_type):
        existing = self.relationship_repository.find_one(relationship)
        if existing and action_type == ACTION_TYPE_SKIP:
            print('Importing is skipped because the relationship exists in neo4j.')
            return existing

        return self.relationship_repository.save(relationship)
            
