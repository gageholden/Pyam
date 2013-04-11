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
require(plyr)

inducePyam <- function(pyamScript,parameterString=""){

#inducePyam <- function(pyamScript,L=0.5,R=5,S=1){
  induce <- "python ./Induce.py"
#  test <- paste(unlist(pyamScript), collapse="\n")
  test <- pyamScript
  command<-paste(induce,parameterString)
  tryCatch(system(command, intern = TRUE, input = test),
           warning=function(w) {
             print("problem values:", command, "\n")
             ok <<- FALSE
           }
  )
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
  
  tryCatch(json_file <- system(command, intern = TRUE),
           warning=function(w) {
             print("problem values:", command, "\n")
             ok <<- FALSE
           }
  )
  
  #json_file <- system(command,intern = TRUE)
  json_data <- fromJSON(paste(json_file, collapse=""))
  json_data
}

fromPyam <- function(filename){
  file <- read.delim(filename, sep = "\n", comment.char = "#", header = FALSE)
  inducePyam(file)
}

getSimilarity <- function(comparison,parameters){
  run <- data.frame("metadata"=comparison$metadata,
             "script"=paste(comparison$script, collapse="\n"))
  run <- cbind(run,t(parameters),deparse.level=2)
  parameterString <- paste("-",names(parameters)," ",parameters,sep="",collapse=" ")
  run$similarity <- as.numeric(inducePyam(comparison[['script']],parameterString)[[1]])
  run
}

similaritiesFromCSV <- function(filename,start=-1,end=-1,parametersIn){
  comparisons <- fromCSV(filename, start,end)
  comparisons <- (lapply(comparisons,getSimilarity, parameters=parametersIn))
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

getData <- function(parameters,startIn=-1,endIn=-1){
  if(length(parameters)==2){
    print(names(parameters)[1])
    param = expand.grid(names(parameters)=pararameters[[1]],names(par)=par[[2]])
    print(param)
    colnames(param)<-colnames(parameters)
    ldply(
      unlist(
        apply(param,1,
               function(x){similaritiesFromCSV(myTempFilename,start=startIn,end=endIn,parametersIn=x)}),
        recursive = F),function(x){x})
  }else{
    param = expand.grid(parameters[[1]],parameters[[2]],parameters[[3]])
    colnames(param)<-colnames(parameters)
    ldply(
      unlist(
        apply(param,1,
              function(x){similaritiesFromCSV(myTempFilename,start=startIn,end=endIn,parametersIn=x)}),
        recursive = F),function(x){x})
  }
}

par <- list("r"=seq(0,25,by=1),"l"=seq(0.05,1,by=0.05))
#LOOK AT colwise! plyr!