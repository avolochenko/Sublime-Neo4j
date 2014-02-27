import sublime, sublime_plugin, time
import urllib.request, urllib.error, urllib.parse, json, re


HEADERS = {'content-type': 'application/json'}

CYPHER_QUERY ={
    "query" : "",
    "params" : {
    }
}

class Neo4jCommand(sublime_plugin.TextCommand):

    def run(self,  edit):
      start_time = time.time()
      s = sublime.load_settings("Neo4j.sublime-settings")

      #grab selections, in this case only one selection
      #sublime supports multi selections
      selections = self.view.sel()
      
      #assing text from selection to the query object
      if self.view.substr(selections[0]):
        text = self.view.substr(selections[0])
      else:
        text = self.view.substr(self.view.visible_region())

      for query in text.split(";"):
        if query.strip() == '':
          continue #Skip trailing queries, and ignore any that had ;; somewhere

        CYPHER_QUERY["query"] = query
        #convert into proper json
        data = json.dumps(CYPHER_QUERY)

        # POST to neo4j cypher REST api
        try:
          req = urllib.request.Request(s.get("neo4j_api"), data.encode('utf-8'), HEADERS)
          response = urllib.request.urlopen(req)
          response_json = json.loads(response.read().decode('utf-8'))
          response.close()

          column_count = len(response_json['columns'])
          Column = Table.Column
          table = []
          rows = [[] for _ in range(column_count)]

          if column_count > 0:
            # parse json document and create a pretty table        
            for x in range(0,column_count ):
              for row in response_json['data']:
                rows[x].append(str(row[x]['data']))

              table.append( Column(response_json['columns'][x],rows[x] ) )
            end_time = time.time()
            print(Table( *tuple(table) ))
          else:
            end_time = time.time()
            print("No results returned")
          print("Neo4j: query took ({0}) seconds".format(end_time-start_time))

          response.close()
        
        except urllib.error.HTTPError as h:
          print('Neo4j: http error - {0} {1}'.format(h.code,h.reason))

        except urllib.error.URLError as e:
          print('Neo4j: url error - {0}'.format(e.reason))


# Pretty table class
# reference: http://code.activestate.com/recipes/577202-render-tables-for-text-interface/
class Table:
    def __init__(self, *columns):
        self.columns = columns
        self.length = max(len(col.data) for col in columns)
    def get_row(self, rownum=None):
        for col in self.columns:
            if rownum is None:
                yield col.format % col.name
            else:
                yield col.format % col.data[rownum]
    def get_line(self):
        for col in self.columns:
            yield '-' * (col.width + 2)
    def join_n_wrap(self, char, elements):
        return ' ' + char + char.join(elements) + char
    def get_rows(self):
        yield self.join_n_wrap('+', self.get_line())
        yield self.join_n_wrap('|', self.get_row(None))
        yield self.join_n_wrap('+', self.get_line())
        for rownum in range(0, self.length):
            yield self.join_n_wrap('|', self.get_row(rownum))
        yield self.join_n_wrap('+', self.get_line())
    def __str__(self):
        return '\n'.join(self.get_rows())
    class Column():
        LEFT, RIGHT = '-', ''
        def __init__(self, name, data, align=RIGHT):
            self.data = data
            self.name = name
            self.width = max(len(x) for x in data + [name])
            self.format = ' %%%s%ds ' % (align, self.width)


