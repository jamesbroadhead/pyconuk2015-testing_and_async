def merge_with_database(body, key):
    data = self.database.get(key)
    merged = merge_results(data, body)
    self.database.write(key, merged)
    return