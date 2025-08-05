from neo4j import GraphDatabase
import json
import re

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "testingsmartlink123")
)

def load_bios(jsonl_path="ingest/parsed_bios.jsonl"):
    with open(jsonl_path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def extract_entity_regex(text, pattern):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else None

def push_to_neo4j(bios):
    with driver.session() as session:
        for bio in bios:
            user_id = bio.get("user_id")
            text = bio.get("bio", "")

            try:
                if " is a " in text:
                    name = text.split(" is a ")[0].strip()
                    role = extract_entity_regex(text, r"is a (.+?) at")
                    company = extract_entity_regex(text, r"at (.+?) based") or extract_entity_regex(text, r"at (.+?)(?: based|$)")
                elif " works as a " in text:
                    name = text.split(" works as a ")[0].strip()
                    role = extract_entity_regex(text, r"works as a (.+?) at")
                    company = extract_entity_regex(text, r"at (.+?) based") or extract_entity_regex(text, r"at (.+?)(?: based|$)")
                else:
                    print(f"[WARN] Skipping bio: {text}")
                    continue

                location = extract_entity_regex(text, r"based in ([^,\.]+)")
                school = extract_entity_regex(text, r"studied at ([^,\.]+)")

                print(f"[DEBUG] user_id={user_id}, name={name}, role={role}, company={company}, location={location}, school={school}")

                session.run("""
                    MERGE (p:Person {user_id: $user_id, name: $name})
                    MERGE (r:Role {name: $role})
                    MERGE (c:Company {name: $company})
                    MERGE (p)-[:HAS_ROLE]->(r)
                    MERGE (p)-[:WORKS_AT]->(c)
                    FOREACH (_ IN CASE WHEN $location IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (l:Location {name: $location})
                        MERGE (p)-[:BASED_IN]->(l)
                    )
                    FOREACH (_ IN CASE WHEN $school IS NOT NULL THEN [1] ELSE [] END |
                        MERGE (s:School {name: $school})
                        MERGE (p)-[:STUDIED_AT]->(s)
                    )
                """, user_id=user_id, name=name, role=role, company=company,
                     location=location, school=school)

            except Exception as e:
                print(f"[ERROR] Failed to process: {text}")
                print(f"        Reason: {e}")
                continue

    print("[SUCCESS] Pushed bios with school and location to Neo4j.")

if __name__ == "__main__":
    bios = load_bios()
    push_to_neo4j(bios)
