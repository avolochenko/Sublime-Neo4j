# Sublime Text 2/3 plugin: Neo4j

* Sublime is one of the best cross platform editors, so i thought why not create a simple Neo4j plugin so here it is.
* Solves the problem of running Neo4j queries from terminal and not being able to save/manage your query files in one place
* This is a very rough draft of the plugin, will add features if time permits, others are welcome to add to this project.


#Installation:
* Just make a clone of the repo into your ~/Library/Application Support/Sublime Text 3/Packages or equivalent on Windows/Linux.
* Edit Neo4j.sublime-settings (accessible through the Preferences -> Package Settings -> Neo4j Menu)
  * Edit the url (default localhost)
  * Edit the username and password (default neo4j:neo)
* Results are displayed in the console (Ctrl+~) to open Console
* Default query run key is ctrl+r , just select query and hit ctrl+r. Edit Default.sublime-keymap if you need to change this.

# Cypher
There's really great cypher syntax highlight plugin named Cypher by Jan-Klass Kollhof which can be installed using Package Manager.
Search for Cypher in Package Manager, also nice install video tutorial by Peter Neubauer http://vimeo.com/64886333

Thanks for looking!

![Alt text](/sublime-text-neo4j.png "Sublime Neo4j Plugin")
