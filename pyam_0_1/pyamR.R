if(Sys.info()["user"]=="dlandy"){
  setwd("/Users/dlandy/programs/Pyam/pyam_0_1")
  Windows <- FALSE
} else {
  if(Sys.info()["sysname"]=="Windows"){
    setwd("C:\\Users\\Gage\\Documents\\GitHub\\Pyam\\pyam_0_1")
    Windows <- TRUE 
  }else{
    setwd("/Users/gageholden/Desktop/Pyam/pyam_0_1")
    Windows <- FALSE
  }
}
require(plyr)

inducePyam <- function(pyamScript){
  system("python ./Induce.py", intern = TRUE, input = pyamScript)
}

fromCSV <- function(filename, start=-1, end=-1){
  library("rjson")
  
  command<-paste("python ./csvToPyam.py ", filename)
  if(start != -1){
    command <- paste(command, " -s ", start)
  }
  if(end != -1){
    command <- paste(command, " -e ", end)
  }
           
  json_file <- system(command,intern = TRUE)
  json_data <- ldply(fromJSON(paste(json_file, collapse="")), data.frame)
  json_data
}

runScriptFile <- function(filename){
  file <- read.delim(filename, sep = "\n", comment.char = "#", header = FALSE)
  inducePyam(file)
}

nameParameters <- function(parameters){
  names(parameters)<-c(
    'l',
    'r',
    'fif',
    'fcf',
    'oio',
    'oco',
    'rir',
    'rcr',
    'ocf',
    'fco',
    'ocr',
    'rco',
    'fmismatch',
    'rmismatch',
    'fwmatch',
    'fwmis',
    'rwmatch',
    'rwmis'
    )
  parameters
}

checkDifference <- function(parameters, humanData, comparisons){
  parameters <- nameParameters(parameters)
  print(parameters)
  if(mean(parameters>=0)==1&parameters['fmismatch']<=1&parameters['rmismatch']<=1&parameters['l']<=1
     &parameters['r']>=1){
    comparisons<-appendSimilarities(comparisons,parameters)

    differences<-abs(arrange(humanData,itemNumber)$similarity-arrange(comparisons,itemNumber)$similarity)
    exp(mean(log(differences[differences!=0])))
  }else{
    100000000000
  }
}
counter = 0
#steplist = data.frame()
checkDifferenceFast <- function(parameters, humanData, comparisons){
  parameters <- nameParameters(parameters)
  #print(parameters)
  #print(humanData$sID[1])
  #steplist<<-rbind(steplist,parameters)
  #print(steplist)
  if(mean(parameters>=0)==1&parameters['fmismatch']<=1&parameters['rmismatch']<=1&parameters['l']<=1
     &parameters['r']>=1&parameters['r']<=100){
    comparisons<-appendSimilaritiesFast(comparisons,parameters)
    differences<-abs(arrange(humanData,itemNumber)$similarity-arrange(comparisons,itemNumber)$similarity)
    exp(mean(log(differences[differences!=0])))
  }else{
    100000000000
  }
}

appendSimilaritiesFast <- function(comparisons,parameters){
  paramLine<-paste("set", paste(names(parameters),parameters,collapse=", "))
  comparisons <- cbind(comparisons,t(parameters),deparse.level=2)
  comparisons<-mutate(comparisons,script=paste(paramLine,script,sep="\n"))
  comparisons<-mutate(arrange(comparisons,itemNumber),
                      similarity = as.numeric(inducePyam(paste(arrange(comparisons,itemNumber)$script,collapse="\n"))))
}

appendSimilarities <- function(comparisons,parameters){
  paramLine<-paste("set", paste(names(parameters),parameters,collapse=", "))
  comparisons <- cbind(comparisons,t(parameters),deparse.level=2)
  comparisons<-mutate(comparisons,script=paste(paramLine,script,sep="\n"))
  ddply(.data=comparisons,c("script"), mutate, similarity = as.numeric(inducePyam(as.character(script))))
}

getSimilarities <- function(comparisons,parameters){
  paramLine<-paste("set", paste(names(parameters),parameters,collapse=", "))
  comparisons <- cbind(comparisons,t(parameters),deparse.level=2)
  comparisons<-mutate(comparisons,script=paste(paramLine,script,sep="\n"))
  comparisons<-ddply(.data=comparisons,c("script"), mutate, similarity = as.numeric(inducePyam(as.character(script))))
  comparisons$similarity
}

makeGraph <- function(comparisons,xAxis,yAxis){
    plot(cbind(lapply(comparisons,function(x){x[[xAxis]]}),lapply(comparisons,function(x){x[[yAxis]]})),xlab=xAxis,ylab=yAxis)
}


multmerge <- function(mypath){
  filenames=list.files(path=mypath, full.names=TRUE)
  datalist = ldply(filenames, function(x){read.delim(file=x,header=T)})
}

#These are the stimuli files that have to be read in
#sLarkey = fromCSV("./data/StimuliLarkey_stim.csv")
#sPairs = fromCSV("./data/")
#sTwo = fromCSV("./data/")
smLarkey = fromCSV("./data/StimuliLarkey_mips.csv")

#These are (I believe) the correct human data files
#hLarkey = read.csv("./data/ANA-Larkey.csv")
hPairs = read.csv("./data/ANA-2-Timed.csv")
hTwo = read.csv("./data/ANA-1.csv")

hLarkey <- multmerge("./data/ANA-Larkey-Human-Correct/")

hLarkey<-mutate(hLarkey,similarity = as.numeric(response)/10)
#checkDifference(c(1,20,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1),hLarkey,sLarkey)
#optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifference, humanData=hLarkey, comparisons=sLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=50), method="SANN")-> outSANN


#mipsSim<-appendSimilarities(smLarkey,nameParameters(c(1,100,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1)))
#plot(hLarkey$itemNumber[hLarkey$sID==18], hLarkey$similarity[hLarkey$sID==18])
#plot(mipsSim$itemNumber, mipsSim$similarity)
#mipsSim[mipsSim$itemNumber==79,]$script;hLarkey[hLarkey$itemNumber==79,][1:5,]

#Reduce(function(y,z){ldply(unique(hLarkey$sID),function(x){optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifferenceFast, humanData=hLarkey[hLarkey$sID==x,], comparisons=smLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=10), method="SANN")->record;append(nameParameters(record$par),c("value"=record$value,"sID"=x))})},seq(1,10))
#ldply(unique(hLarkey$sID),function(x){optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifferenceFast, humanData=hLarkey[hLarkey$sID==x,], comparisons=smLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=500), method="SANN")->record;append(nameParameters(record$par),c("value"=record$value,"sID"=x))})->500_sID

#ldply(unique(hLarkey$sID),function(x){optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifferenceFast, humanData=hLarkey[hLarkey$sID==x,], comparisons=smLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=500), method="SANN")->record;append(nameParameters(record$par),c("value"=record$value,"sID"=x))})->sID_500
#x=26;steplist=data.frame();optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifferenceFast, humanData=hLarkey[hLarkey$sID==x,], comparisons=smLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=500), method="SANN")->record;append(nameParameters(record$par),c("value"=record$value,"sID"=x))->record