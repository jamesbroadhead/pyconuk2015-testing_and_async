def merge_with_database(body, key):
    deferred = self.database.get(key)
    deferred.addCallback(merge_results, body)
    deferred.addCallback(lambda merged:
      self.database.write(key, merged))
    return deferred
