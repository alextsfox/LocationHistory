library(tidyverse)
library(ggplot2)
library(plotly)
library(maps)
library(lubridate)
library(anytime)
options(digits = 11)

# OPT 1:if running for first time with this data:
loc_list_full_1 <- read.csv('csv-files/FilteredLocations_20190214_Full.csv')
loc_list_full_2 <- read.csv('csv-files/FilteredLocations_20190807_Full.csv')
loc_list_full_3 <- read.csv('csv-files/FilteredLocations_20191128_Full.csv')
loc_list_full_4 <- read.csv('csv-files/FilteredLocations_20200227_Full.csv')
loc_list_full_5 <- read.csv('csv-files/FilteredLocations_20200429_Full.csv')
loc_list_full_6 <- read.csv('csv-files/FilteredLocations_20200814_Full.csv')
loc_list_full_7 <- read.csv('csv-files/FilteredLocations_20201229_Full.csv')

loc_list_full <- rbind(loc_list_full_1, loc_list_full_2, loc_list_full_3, loc_list_full_4, loc_list_full_5, loc_list_full_6, loc_list_full_7)
loc_list_full <- loc_list_full[!duplicated(loc_list_full$time), ]
rm(loc_list_full_1)
rm(loc_list_full_2)
rm(loc_list_full_3)
rm(loc_list_full_4)
rm(loc_list_full_5)
rm(loc_list_full_6)
rm(loc_list_full_7)

loc_list_full <- loc_list_full %>%
  #mutate(date_time = as.Date(as.POSIXct(time, origin="1970-01-01-00-00-00")))
  mutate(date_time = anytime(time, asUTC=TRUE)) %>%  # convert timestamp to ymd_hms
  mutate(dec_year = decimal_date(anytime(date_time, asUTC=TRUE)))  # convert ymd_hms to decimal (many sig figs)

write.csv(loc_list_full, 'csv-files/FilteredLocations_Full_Merged.csv')

# OPT 2: otherwise, run this instead:
loc_list_full <- read.csv('csv-files/FilteredLocations_Full_Merged.csv')

# mardi himal timestamp marked by index 999999 and timestamp 1577295001 - 1577295005
mardi_list <- read.csv('csv-files/FilteredLocations_Full_Merged_Mardi_Himal.csv')

loc_list_full$alt[loc_list_full$alt == -9999] <- NaN
mardi_list$alt[mardi_list$alt == -9999] <- NaN
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

#Mtn West
N <- 50
S <- 35
E <- -104
W <- -115

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

# Western MA
N <- 42.645
S <- 41.814
E <- -72.272
W <- -73.592

# STL
N <- 39.032
S <- 38.14
E <- -89.611
W <- -91.2353

# NRG
N <- 38.3279
S <- 37.9220
E <- -80.7246
W <- -81.2468

# Albany County
N <- 41.4291
S <- 40.7608
E <- -105.1777
W <- -106.3750

# every 10 datapoints
step_size = 1
ggplot(data = loc_list_full %>% filter(X %% step_size == 0 & lat <= N & lat >= S & lon >= W & lon <= E & dec_year >= start & dec_year <= end)) +
  geom_point(mapping = aes(x = lon, y = lat, color = dec_year), size = 0.7) +
  scale_y_continuous(limits = c(S,N)) +
  scale_x_continuous(limits = c(W,E)) +
  #borders("world", xlim = c(W,E), ylim = c(S,N)) +
  #borders("world", xlim = c(W,E), ylim = c(S,N)) +
  #borders("state", alpha = 0.2) +
  #coord_quickmap() +
  scale_color_gradient(low = 'blue', high = 'red')+
  theme_bw()

# altitude data inc. mardi himal
ggplot(data = mardi_list %>% filter(dec_year >= start & dec_year <= end)) +
  geom_point(mapping = aes(x = dec_year, y = alt), size=0.1)+#ymin = alt - acc, ymax = alt + acc), size = 0.001) +
  ylim(-100, 4750) +
  ggtitle("Elevation over time") +
  xlab("Date") +
  ylab("Elevation (m)") +
  scale_x_continuous(breaks = seq(from = decimal_date(ymd_hms("2017-03-02 20:00:00 UTC")), 
                                  to = decimal_date(ymd_hms("2021-01-01 00:00:00 UTC")), 
                                  by = 0.08333333333333333),
                   labels=c(               'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 
                            '2018 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 
                            '2019 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 
                            '2020 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', 
                            '2021 J')) +
  theme_bw(base_size=15)+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  xlim(decimal_date(ymd_hms("2018-06-04 00:00:00 UTC")), decimal_date(ymd_hms("2018-08-21 00:00:00 UTC")))

# altitude data NOT inc. mardi himal
ggplot(data = loc_list_full %>% filter(X %% step_size == 0))+# & dec_year >= start & dec_year <= end)) +
  geom_pointrange(mapping = aes(x = dec_year, y = alt, ymin = alt - acc, ymax = alt + acc), size = 0.02) +
  xlim(2017.25, 2020.75) +
  ylim(-100, 4750) +
  ggtitle("Elevation over time") +
  xlab("Date") +
  ylab("Elevation (m)") +
  #scale_x_continuous(breaks = seq(from = 2017.25, to = 2020.25, by = 0.25),
  #               labels=c('Apr', 'Jul', 'Oct', '2018', 'Apr', 'Jul', 'Oct', '2019', 'Apr', 'Jul', 'Oct', '2020', 'Apr')) +
  scale_x_continuous(breaks = seq(from = 2017.16666666666667, to = 2020.8, by = 0.08333333333333333),
                     labels=c('M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2018 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2019 J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D', '2020 J', 'F', 'M', 'A', 'M','J','J','A','S','O')) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
