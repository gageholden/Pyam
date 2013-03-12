if(Sys.info()["sysname"]=="Windows"){
  setwd("C:\\Users\\Gage\\Desktop\\Pyam\\pyam_0_1")
  Windows <- TRUE 
}else{
  setwd("/Users/gageholden/Desktop/Pyam/pyam_0_1")
  Windows <- FALSE
}
inducePyam <- function(pyamScript,parameterString=""){
  induce <- "python ./Induce.py"
  test <- paste(unlist(pyamScript), collapse="\n")
  command<-paste(induce,parameterString)
  #print(command)
  system(command, intern = TRUE, input = test)
  #as.numeric(system(command, intern = TRUE))
  
  #data.frame(sim=c)
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
  comparisons <- lapply(comparisons,parameters=parametersIn,getSimilarity)
  comparisons
}

myTempFilename = "./data/StimuliLarkey_mips.csv"

interestingPlot <- function(){
  runtest = lapply(1:20,function(x){similaritiesFromCSV(myTempFilename,start=1,end=1,parametersIn=list("r"=x, "l"=0.2))})
  plot(cbind(lapply(runtest,function(x){x[[1]]$parameters$r}),lapply(runtest,function(x){x[[1]]$similarity})),xlab="Rounds",ylab="Similarity")
}