class Token():
    def __init__(self, token_type, token_value, start_position):
        self.token_type = token_type
        self.token_value = token_value
        self.start_position = start_position

    def get_json_node(self):
        node = {}
        node['token'] = self.token_type
        node['value'] = self.token_value
        node['start_position'] = self.start_position
        node['length'] = len(self.token_value)
        return node