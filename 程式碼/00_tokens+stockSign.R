###---------------------------------------###
###--------ptt斷詞後重新篩選開市日--------
###---------------------------------------###

### 一、讀檔：讀入口罩類、檢測試劑類、疫苗類漲跌，六種斷詞讀檔
### 二、合併tokens與股票漲跌(函式、執行)
### 三、去除空值、存檔

library(readxl)
library(tibble)
library(dplyr)

## 口罩類漲跌
df_mask_stocks <- as_tibble(read_excel("mask_stocks.xlsx")) %>%
    select(1, 15) %>%
    rename(date = 康那香, 漲跌 = ...15)
df_mask_stocks <- df_mask_stocks[2:340, ] %>%
    mutate(date = as.Date(date)) %>%
    arrange(date) %>%
    mutate(rise = ifelse(漲跌 == "漲", 1, ifelse(漲跌 == "平", 0, -1)))

View(df_mask_stocks)

## 檢測試劑類漲跌
df_testKits_stocks <- as_tibble(read_excel("testKits_stocks.xlsx")) %>%
    select(1, 12) %>%
    rename(date = 瑞基)
df_testKits_stocks <- df_testKits_stocks[2:340, ] %>%
    mutate(date = as.Date(date)) %>%
    arrange(date) %>%
    mutate(rise = ifelse(漲跌 == "漲", 1, ifelse(漲跌 == "平", 0, -1)))

View(df_testKits_stocks)

## 疫苗類漲跌
df_vaccine_stocks <- as_tibble(read_excel("vaccine_stocks.xlsx")) %>%
    select(1, 9) %>%
    rename(date = 國光生)
df_vaccine_stocks <- df_vaccine_stocks[2:340, ] %>%
    mutate(date = as.Date(date)) %>%
    arrange(date) %>%
    mutate(rise = ifelse(漲跌 == "漲", 1, ifelse(漲跌 == "平", 0, -1)))

View(df_vaccine_stocks)


## tokens 讀檔
covid_token_df <- as_tibble(readr::read_csv("../tokens+cvaw/covid_token.csv")) %>%
    select(-1)
covid_CKIPtoken_df <- as_tibble(readr::read_csv("../tokens+cvaw/covid_CKIPtoken.csv")) %>%
    select(-1)
covid_CKIP_nonEng_df <- as_tibble(readr::read_csv("../tokens+cvaw/covid_CKIP_nonEng.csv")) %>%
    select(-1)
stock_token_df <- as_tibble(readr::read_csv("../tokens+cvaw/stock_token.csv")) %>%
    select(-1)
stock_CKIPtoken_df <- as_tibble(readr::read_csv("../tokens+cvaw/stock_CKIPtoken.csv")) %>%
    select(-1)
stock_CKIP_nonEng_df <- as_tibble(readr::read_csv("../tokens+cvaw/stock_CKIP_nonEng.csv")) %>%
    select(-1)

## cvaw 讀檔
cvaw_covid_df <- as_tibble(readr::read_csv("../tokens+cvaw/cvaw_covid.csv")) %>%
    select(-1) %>%
    rename(date = Date)
cvaw_stock_df <- as_tibble(readr::read_csv("../tokens+cvaw/cvaw_stock.csv")) %>%
    select(-1) %>%
    rename(date = Date)


## 合併tokens與股票漲跌(函式)
combine_tokens_stocks <- function(df_tokens){
    
    # 建立vector儲存該文本的股票漲跌
    stockRise_mask = rep(NA, times = length(df_tokens$date))
    stockRise_testKits = rep(NA, times = length(df_tokens$date))
    stockRise_vaccine = rep(NA, times = length(df_tokens$date))
    
    # 每個股票日期跑一次
    for (i in seq(length(df_mask_stocks$date))){
        dateA = df_mask_stocks$date[i]
        riseSign_mask = df_mask_stocks$rise[i]
        riseSign_testKits = df_testKits_stocks$rise[i]
        riseSign_vaccine = df_vaccine_stocks$rise[i]
        
        # 針對同一個股票日期，每一個文本檢查日期+1是否符合此股票日期(dateA)
        # 預測文本後一天的股票漲跌
        for (j in seq(length(df_tokens$date))){
            # 用前一天文本來預測股票
            dateB = df_tokens$date[j] + 1
            
            if (dateA == dateB){
                
                stockRise_mask[j] <- riseSign_mask
                stockRise_testKits[j] <- riseSign_testKits
                stockRise_vaccine[j] <- riseSign_vaccine
            }
        }
    }
    # 去除非開市日(沒有股票漲跌者)
    df_tokens_stock <- cbind(df_tokens, stockRise_mask, stockRise_testKits, stockRise_vaccine) %>%
        filter(!is.na(stockRise_mask)) 
    
    return(df_tokens_stock)
}


## 原始斷詞檔加入股票漲跌篩選有開市日
covid_token_stockSign_df <- combine_tokens_stocks(covid_token_df)
covid_CKIPtoken_stockSign_df <- combine_tokens_stocks(covid_CKIPtoken_df)
covid_CKIP_nonEng_stockSign_df <- combine_tokens_stocks(covid_CKIP_nonEng_df)
stock_token_stockSign_df <- combine_tokens_stocks(stock_token_df)
stock_CKIPtoken_stockSign_df <- combine_tokens_stocks(stock_CKIPtoken_df)
stock_CKIP_nonEng_stockSign_df <- combine_tokens_stocks(stock_CKIP_nonEng_df)

cvaw_covid_stockSign_df <- combine_tokens_stocks(cvaw_covid_df)
cvaw_stock_stockSign_df <- combine_tokens_stocks(cvaw_stock_df)


## 去除空值(token, CKIP_nonEng 的空值較 CKIPtoken 多)
covid_na <- covid_token_stockSign_df$id[is.na(covid_token_stockSign_df$content) == T]
stock_na <- stock_token_stockSign_df$id[is.na(stock_token_stockSign_df$content) == T]

covid_token_stockSign_df <- covid_token_stockSign_df %>%
    filter(!(id %in% covid_na))
covid_CKIPtoken_stockSign_df <- covid_CKIPtoken_stockSign_df %>%
    filter(!(id %in% covid_na))
covid_CKIP_nonEng_stockSign_df <- covid_CKIP_nonEng_stockSign_df %>%
    filter(!(id %in% covid_na))
stock_token_stockSign_df <- stock_token_stockSign_df %>%
    filter(!(id %in% stock_na))
stock_CKIPtoken_stockSign_df <- stock_CKIPtoken_stockSign_df %>%
    filter(!(id %in% stock_na))
stock_CKIP_nonEng_stockSign_df <- stock_CKIP_nonEng_stockSign_df %>%
    filter(!(id %in% stock_na))

cvaw_covid_stockSign_df <- cvaw_covid_stockSign_df %>%
    filter(!(id %in% covid_na))
cvaw_stock_stockSign_df <- cvaw_stock_stockSign_df %>%
    filter(!(id %in% stock_na))


## 篩選過後檔案存檔
write.csv(covid_token_stockSign_df, file = "covid_token_stockSign.csv", fileEncoding = "UTF-8")
write.csv(covid_CKIPtoken_stockSign_df, file = "covid_CKIPtoken_stockSign.csv", fileEncoding = "UTF-8")
write.csv(covid_CKIP_nonEng_stockSign_df, file = "covid_CKIP_nonEng_stockSign.csv", fileEncoding = "UTF-8")
write.csv(stock_token_stockSign_df, file = "stock_token_stockSign.csv", fileEncoding = "UTF-8")
write.csv(stock_CKIPtoken_stockSign_df, file = "stock_CKIPtoken_stockSign.csv", fileEncoding = "UTF-8")
write.csv(stock_CKIP_nonEng_stockSign_df, file = "stock_CKIP_nonEng_stockSign.csv", fileEncoding = "UTF-8")

write.csv(cvaw_covid_stockSign_df, file = "cvaw_covid_stockSign.csv", fileEncoding = "UTF-8")
write.csv(cvaw_stock_stockSign_df, file = "cvaw_stock_stockSign.csv", fileEncoding = "UTF-8")
