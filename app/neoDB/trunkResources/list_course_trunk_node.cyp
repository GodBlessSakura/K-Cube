MATCH (trunk:Trunk)
WHERE split(trunk.deltaGraphId,'.')[0] = replace($courseCode,' ' ,'_')
WITH DISTINCT trunk, EXISTS((:GraphConcept{name: $courseCode})-[:COURSE_DESCRIBE]-()<-[:TRUNK_DESCRIBE]-(trunk)) as isActive
RETURN trunk AS nodes, isActive
