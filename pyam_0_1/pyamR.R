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
    differences<-abs(humanData$similarity[order(humanData$itemNumber)]-as.numeric(comparisons$similarity[order(comparisons$itemNumber)]))
    exp(mean(log(differences[differences!=0])))
  }else{
    100000000000
  }
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

#These are the stimuli files that have to be read in
sLarkey = fromCSV("./data/StimuliLarkey_stim.csv")
#sPairs = fromCSV("./data/")
#sTwo = fromCSV("./data/")
smLarkey = fromCSV("./data/StimuliLarkey_mips.csv")

#These are (I believe) the correct human data files
hLarkey = read.csv("./data/ANA-Larkey.csv")
hPairs = read.csv("./data/ANA-2-Timed.csv")
hTwo = read.csv("./data/ANA-1.csv")

hLarkey<-mutate(hLarkey,similarity = as.numeric(Rating)/10)
#checkDifference(c(1,20,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1),hLarkey,sLarkey)
#optim(par=c(0.5,10,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1), checkDifference, humanData=hLarkey, comparisons=sLarkey, control=list(parscale=c(1,20,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), maxit=50), method="SANN")-> outSANN

hLarkey$Shape.method <- unlist(tapply(1:9, 1:9, function(x){rep(hLarkey$Color.method[x], 9)}) )
hLarkey$Shape.method <- factor(hLarkey$Shape.method2, levels=c("AB","BA",    "AA", "BB", "AC", "CA",  "BC" , "CB", "CD"))
hLarkey$Color.method <- factor(hLarkey$Color.method, levels=c("AB","BA",    "AA", "BB", "AC", "CA",  "BC" , "CB", "CD"))


# Replication of Larkey & Markman:
#with(hLarkey[hLarkey$Shape.method %in% c("AB", "BA"),], interaction.plot(Color.method, Shape.method, similarity))
smLarkey  <- smLarkey[order(smLarkey$itemNumber),]
smLarkey$Shape.method <- factor(tapply(as.character(hLarkey$Shape.method), hLarkey$itemNumber, unique), levels=c("AB","BA",    "AA", "BB", "AC", "CA",  "BC" , "CB", "CD"))
smLarkey$Color.method <- factor(tapply(as.character(hLarkey$Color.method), hLarkey$itemNumber, unique), levels=c("AB","BA",    "AA", "BB", "AC", "CA",  "BC" , "CB", "CD"))

#mipsSim<-appendSimilarities(smLarkey,nameParameters(c(1,100,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1)))
#mipsSim[mipsSim$itemNumber==79,]$script;hLarkey[hLarkey$itemNumber==79,][1:5,]

# Larkey estimate for this person
#with(mipsSim[mipsSim$Shape.method %in% c("AB", "BA"),], interaction.plot(Color.method, Shape.method, similarity))
