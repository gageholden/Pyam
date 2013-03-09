setwd("/Users/gageholden/Desktop/Pyam/pyam_0_1")
inducePyam <- function(pyamScript,L=0.5,R=5,S=1){
  #print(environment())
  #print(as.list(environment()))
  induce <- "python ./Induce.py"
  test <- paste(unlist(pyamScript), collapse="\n")
  command<-paste("echo ", "\"", test, "\"", " | ", induce,"-l",L,"-r",R,"-s",S)
  #print(command)
  system(command, intern = TRUE)
  #as.numeric(system(command, intern = TRUE))
  
  #data.frame(sim=c)
}

runPyam <- function(filename){
  library("rjson")
  
  command<-paste("python ./csvToPyam.py ", filename)  
  
  json_file <- system(command,intern = TRUE)
  json_data <- fromJSON(paste(json_file, collapse=""))
  json_data
}