# java -Dwebdriver.gecko.driver=./Desktop/RStudio.app/geckodriver -jar desktop/RStudio.app/selenium-server-standalone-3.4.0.jar
#java -Dwebdriver.chrome.driver=./Desktop/RStudio.app/chromedriver -jar desktop/RStudio.app/selenium-server-standalone-3.4.0.jar
#Scraping the daily air quality of China's cities （2014-2017）
require(xlsx)
require(magrittr)
require(rvest)
if (!require('devtools')) install.packages("devtools")
if(!require(RSelenium)) devtools::install_github("ropensci/RSelenium")
remDr <- remoteDriver(remoteServerAddr = "localhost" 
                      , port = 4444L
                      , browserName = "chrome"
)
remDr$open()
remDr$navigate("http://datacenter.mep.gov.cn/index!MenuAction.action?name=402880fb24e695b60124e6973db30011")
Sys.sleep(3)
remDr$findElement(using = 'link text',"大气")$clickElement()
Sys.sleep(1)
remDr$findElement(using = 'link text',"全国城市空气质量日报")$clickElement()
remDr$switchToFrame("iframepage")
remDr$findElement(using = 'xpath',"//*[@id='mainForm']/div[2]/div[2]")$getElementText()
for (s in 300:413){
  remDr$findElement(using = 'link text',"下一页")$clickElement()
}

for (i in 1:100) { 
  if (i==1) { 
    tables<-read_html(remDr$getPageSource()[[1]]) %>% html_table(,fill=TRUE)
    table<-tables[[6]]
    remDr$findElement(using = 'link text',"下一页")$clickElement()
  } else { 
    tables<-read_html(remDr$getPageSource()[[1]]) %>% html_table(,fill=TRUE)
    table<-rbind(table,tables[[2]])
    remDr$findElement(using = 'link text',"下一页")$clickElement()
  } 
} 
AQ1<-rbind(AQ1,table)
save(AQ1,file="~/Desktop/AQ2017.Rdata")
AQ1$ID<-NULL   #删除ID行
newdata<-AQ1[which(AQ1$日期 != "2016-12-31"),]
newdata$序号<-NULL
cnames=paste("v",1:7,sep="")
colnames(newdata)=cnames
library(rio)
export(newdata, "/Users/aj/Desktop/AQ_2017.dta")

#Scraping the daily air quality of China's cities （2000-2013）
require(xlsx)
require(magrittr)
require(rvest)
require(rio)
require(RSelenium)
remDr <- remoteDriver(remoteServerAddr = "localhost" 
                      , port = 4444L
                      , browserName = "chrome"
)
remDr$open()
remDr$navigate("http://datacenter.mep.gov.cn/index!MenuAction.action?name=12345678910123456789")
remDr$findElement(using = 'partial link text',"重点城市空气质量日报")$clickElement()
remDr$switchToFrame("iframepage")
for (i in 1:67) { 
  if (i==1) { 
    tables<-read_html(remDr$getPageSource()[[1]]) %>% html_table(,fill=TRUE)
    table<-tables[[6]]
    remDr$findElement(using = 'link text',"上一页")$clickElement()
  } else { 
    tables<-read_html(remDr$getPageSource()[[1]]) %>% html_table(,fill=TRUE)
    n<-length(tables)
    for (j in 1:n) {
      switch (ncol(tables[[j]])==ncol(table), table<-rbind(table,tables[[j]]))
    }
    remDr$findElement(using = 'link text',"上一页")$clickElement()
  }
}
Sys.sleep(0.1)
save(newdata,file="~/Desktop/Historical.Rdata")
Finaldata<-unique(newdata)
Finaldata<-newdata[!duplicated(newdata), ]
cnames=paste("v",1:6,sep="")
colnames(newdata)=cnames
export(newdata, "/Users/aj/Desktop/AQ_Historical.dta")
#调用python模块
system('/Library/Frameworks/Python.framework/Versions/3.6/bin/python3 /Users/aj/Desktop/1.py')