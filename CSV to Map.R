library(tidyverse)
library(ggplot2)
library(plotly)
library(maps)


# OPT 1:if running for first time with this data:
unix_time_to_decimal_year <- function(time){
  
  y <- as.numeric(substr(as.Date(as.POSIXct(time, origin="1970-01-01")),1,4))
  m <- as.numeric(substr(as.Date(as.POSIXct(time, origin="1970-01-01")),6,7))
  d <- as.numeric(substr(as.Date(as.POSIXct(time, origin="1970-01-01")),9,10))
  
  if(m == 9){
    dec_month <- m + d/30
    dec_year <- y + dec_month/12 - 1/12
  }
  else if(m == 4){
    dec_month <- m + d/30
    dec_year <- y + dec_month/12 - 1/12
  }
  else if(m == 6){
    dec_month <- m + d/30
    dec_year <- y + dec_month/12 - 1/12
  }
  else if(m == 11){
    dec_month <- m + d/30
    dec_year <- y + dec_month/12 - 1/12
  }
  else if(m == 2){
    if (y %% 4 == 0){
      dec_month <- m + d/29
      dec_year <- y + dec_month/12 - 1/12
    }
    else if (y == 2000){
      dec_month <- m + d/28
      dec_year <- y + dec_month/12 - 1/12
    }
    else{
      dec_month <- m + d/28
      dec_year <- y + dec_month/12 - 1/12
    }
  }
  
  else{
    dec_month <- m + d/31
    dec_year <- y + dec_month/12 - 1/12
  }
  
  return(dec_year)
}

loc_list_full_1 <- read.csv('csv-files/FilteredLocations_20190214_Full.csv')
loc_list_full_2 <- read.csv('csv-files/FilteredLocations_20190807_Full.csv')
loc_list_full_3 <- read.csv('csv-files/FilteredLocations_20191128_Full.csv')
loc_list_full_4 <- read.csv('csv-files/FilteredLocations_20200227_Full.csv')

loc_list_full <- rbind(loc_list_full_1, loc_list_full_2, loc_list_full_3, loc_list_full_4)
loc_list_full <- loc_list_full[!duplicated(loc_list_full$time), ]
rm(loc_list_full_1)
rm(loc_list_full_2)
rm(loc_list_full_3)
rm(loc_list_full_4)

loc_list_full <- loc_list_full %>%
  mutate(dec_year = unix_time_to_decimal_year(time),
         date_time = as.Date(as.POSIXct(time, origin="1970-01-01"))
  )

write.csv(loc_list_full, 'csv-files/FilteredLocations_Full_Merged.csv')

# OPT 2: otherwise, run this instead:
loc_list_full <- read.csv('csv-files/FilteredLocations_Full_Merged.csv')
mardi_list <- read.csv('csv-files/FilteredLocations_Full_Merged_Mardi_Himal.csv')

loc_list_full$alt[loc_list_full$alt == -9999] <- NaN
mardi_list$alt[mardi_list$alt ==-9999] <- NaN
mardi_list <- mardi_list %>% 
  filter(alt < 5000 & alt > -100) %>% 
  filter((alt > 1000 & acc < 0.1*alt) | alt <= 1000)

# Time period
start <- 1900
end <- 2100

# World:
N <- 85
S <- -85
E <- 180
W <- -180

# Northern Hemisphere
N <- 85
S <- 0
E <- 180
W <- -180

# SEA
N <- 30
S <- 5
E <- 125
W <- 98

# CONUS: W: -124.848974, S: 24.396308 E: -66.885444, N: 49.384358
N <- 50
S <- 24
E <- -66
W <- -125

#Wyo
N <- 45.1
S <- 40.9
E <- -104
W <- -111.1

#NE
N <- 47.5
S <- 36.5
E <- -66.5
W <- -85

#NYC
N <- 40.94
S <- 40.67
E <- -73.77
W <- -74.05

# every 10 datapoints
step_size = 10
ggplot(data = loc_list_full %>% filter(X %% step_size == 0 & lat <= N & lat >= S & lon >= W & lon <= E & dec_year >= start & dec_year <= end)) +
  geom_point(mapping = aes(x = lon, y = lat, color = dec_year), size = 0.5) +
  scale_y_continuous(limits = c(S,N)) +
  scale_x_continuous(limits = c(W,E)) +
  borders("world", xlim = c(W,E), ylim = c(S,N)) +
  #borders("world", xlim = c(W,E), ylim = c(S,N)) +
  #borders("country", alpha = 0.2) +
  coord_quickmap() +
  scale_color_gradient(low = 'blue', high = 'red')

# altitude data
ggplot(data = mardi_list %>% filter(X %% step_size == 0 & dec_year >= start & dec_year <= end)) +
  geom_pointrange(mapping = aes(x = dec_year, y = alt, ymin = alt - acc, ymax = alt + acc), size = 0.02) +
  xlim(2017.25, 2020.25) +
  ylim(-100, 4750) +
  ggtitle("Elevation over time") +
  xlab("Date") +
  ylab("Elevation (m)") +
  #scale_x_continuous(breaks = seq(from = 2017.25, to = 2020.25, by = 0.25),
  #               labels=c('Apr', 'Jul', 'Oct', '2018', 'Apr', 'Jul', 'Oct', '2019', 'Apr', 'Jul', 'Oct', '2020', 'Apr')) +
  scale_x_continuous(breaks = seq(from = 2017.16666666666667, to = 2020.166666666666667, by = 0.08333333333333333),
                   labels=c('M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2018 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2019 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2020 J', 'F', 'M')) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

