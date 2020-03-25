
run with `python3 fetch_cisapi.py`
may take a while to run (more than 10 min)

result data run for Spring 2020 semester (3/9/20)
https://drive.google.com/drive/folders/1fRbb8RN9YnsrNGM5G_C8wmH1Zw4JDiF6?usp=sharing

Neo4j:

- Nodes
  - (:Course { dept: "CS", num: 411 } )	
  - (:Section { crn: 618234 } )
  - (:Meeting { room: 214, start: "9:00am", end: "9:50am" } )
  - (:Building { name: "Siebel Center" } )
- Relations
  - (:Section)-[:SectionOf]->(:Course)
  - (:Meeting)-[:MeetsFor]->(:Section)
  - (:Meeting)-[:LocatedAt]->(:Building)

TODO: 

- prereqs!
- parse time into date object/int?
- getters for python interface
- remove "Virtual" meetings from the database
- remove "MERGE" in query for speed?