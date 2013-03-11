if(Sys.info()["sysname"]=="Windows"){
  setwd("C:\\Users\\Gage\\Desktop\\Pyam\\pyam_0_1")
  Windows <- TRUE 
}else{
  setwd("/Users/gageholden/Desktop/Pyam/pyam_0_1")
  Windows <- FALSE
}
inducePyam <- function(pyamScript,L=0.5,R=5,S=1){
  #print(environment())
  #print(as.list(environment()))
  induce <- "python ./Induce.py"
  test <- paste(unlist(pyamScript), collapse="\n")
  command<-paste(induce,"-l",L,"-r",R,"-s",S)
  #print(command)
  system(command, intern = TRUE, input = test)
  #as.numeric(system(command, intern = TRUE))
  
  #data.frame(sim=c)
}

fromCSV <- function(filename){
  library("rjson")
  
  command<-paste("python ./csvToPyam.py ", filename)  
  
  json_file <- system(command,intern = TRUE)
  json_data <- fromJSON(paste(json_file, collapse=""))
  json_data
}

fromPyam <- function(filename){
  file <- read.delim(filename, sep = "\n", comment.char = "#", header = FALSE)
  inducePyam(file)
}

getSimilarity <- function(comparison){
  as.numeric(inducePyam(comparison[['script']])[[1]])
}

similaritiesFromCSV <- function(filename,start=-1,end=-1,parameters = list()){
  comparisons <- fromCSV("../../StimuliLarkey_mips.csv")
  similarities <- lapply(a,getSimilarity)
  
  #library(plyr)
  rbind(comparisons,similarities)
}