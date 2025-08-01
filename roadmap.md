# plan2eplus roadmap


## desired flow
- read from plan.json # TODO -> include some starting plans 
- create idf w/ eppy + geomeppy -> idf@rooms
- pull data from idf into visuals -> visuals@rooms
- use visuals@rooms  to add subsurfaces to idf  -> idf@subsurfaces
- pull data from idf@subsurfaces to visuals -> visuals@subsurfaces
- use visuals@subsurfaces to specify the afn + materials + airboundaries (#TODO: is this right?)



## documentation todos
- what is the api for each of these steps? how does one specify things? w/ the builder pattern? 
- doc strings?
- test cases that people can run to get started.. 
- docs w/ marimo? -> running in marimo nb? 
  - paired down E+ installation to support this? 