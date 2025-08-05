from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "testingsmartlink123"

driver = GraphDatabase.driver(uri, auth=(username, password))

with driver.session() as session:
    result = session.run("MATCH (n) RETURN count(n) AS node_count")
    for record in result:
        print("Node count:", record["node_count"])
