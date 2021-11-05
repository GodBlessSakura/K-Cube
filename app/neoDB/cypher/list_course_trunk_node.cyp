MATCH (trunk:Trunk)
WHERE trunk.deltaGraphId CONTAINS replace($courseCode,' ' ,'_')
WITH DISTINCT trunk, EXISTS((:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)) as isActive
RETURN trunk AS nodes, isActive
