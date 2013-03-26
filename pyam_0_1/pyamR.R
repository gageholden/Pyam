if(Sys.info()["user"]=="dlandy"){
  setwd("/Users/dlandy/programs/Pyam/pyam_0_1")
  Windows <- FALSE
} else {
  if(Sys.info()["sysname"]=="Windows"){
    setwd("C:\\Users\\Gage\\Desktop\\Pyam\\pyam_0_1")
    Windows <- TRUE 
  }else{
    setwd("/Users/gageholden/Desktop/Pyam/pyam_0_1")
    Windows <- FALSE
  }
}
inducePyam <- function(pyamScript,parameterString=""){

#inducePyam <- function(pyamScript,L=0.5,R=5,S=1){
  induce <- "python ./Induce.py"
  test <- paste(unlist(pyamScript), collapse="\n")
  command<-paste(induce,parameterString)
  
  system(command, intern = TRUE, input = test)
}

fromCSV <- function(filename, start, end){
  library("rjson")
  
  command<-paste("python ./csvToPyam.py ", filename)
  if(start != -1){
    command <- paste(command, " -s ", start)
  }
  if(end != -1){
    command <- paste(command, " -e ", end)
  }
  
  json_file <- system(command,intern = TRUE)
  json_data <- fromJSON(paste(json_file, collapse=""))
  json_data
}

fromPyam <- function(filename){
  file <- read.delim(filename, sep = "\n", comment.char = "#", header = FALSE)
  inducePyam(file)
}

getSimilarity <- function(comparison,parameters){
  run = list("parameters"=parameters,"metadata"=comparison$metadata,
             "script"=comparison$script)
  parameterString <- paste("-",names(parameters)," ",parameters,sep="",collapse=" ")
  run$similarity <- as.numeric(inducePyam(comparison[['script']],parameterString)[[1]])
  run
}

similaritiesFromCSV <- function(filename,start=-1,end=-1,parametersIn = list()){
  comparisons <- fromCSV(filename, start,end)
  comparisons <- lapply(comparisons,getSimilarity, parameters=parametersIn)
  comparisons
}

myTempFilename = "./data/StimuliLarkey_mips.csv"

makeGraph <- function(comparisons,xAxis,yAxis,xMeta = FALSE, yMeta = FALSE){
  if(yMeta && xMeta)
    plot(cbind(lapply(comparisons,function(x){x$metadata[[xAxis]]}),lapply(comparisons,function(x){x$metadata[[yAxis]]})),xlab=xAxis,ylab=yAxis)
  else if(xMeta)
    plot(cbind(lapply(comparisons,function(x){x$metadata[[xAxis]]}),lapply(comparisons,function(x){x[[yAxis]]})),xlab=xAxis,ylab=yAxis)
  else if(yMeta)
    plot(cbind(lapply(comparisons,function(x){x[[xAxis]]}),lapply(comparisons,function(x){x$metadata[[yAxis]]})),xlab=xAxis,ylab=yAxis)
  else
    plot(cbind(lapply(comparisons,function(x){x[[xAxis]]}),lapply(comparisons,function(x){x[[yAxis]]})),xlab=xAxis,ylab=yAxis)
}

getData <- function(){
  unlist(lapply(1:20,function(x){similaritiesFromCSV(myTempFilename,start=1,end=10,parametersIn=list("r"=x, "l"=0.2))}),recursive = F)
}