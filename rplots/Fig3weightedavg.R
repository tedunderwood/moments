# Make unweighted meantime graph
library(ggplot2)
library(dplyr)
times <- read.csv('/Users/tunder/Dropbox/python/time/averagetimes.csv')
fic <- filter(times, col != 'red')
timebreaks = c(-4.82, -2.81, -1.43, 0.365, 1.75, 3.7, 5.08, 7.650835, 10.65)
timelabels = c('2 min', '15 min', 'an hour', '6 hours', 'a day', 'a week', 'a month', 'a year', '20 years')
fic$colors <- rep('black', length(fic$col))
fic$colors[fic$title == "Gulliver's Travels into Several Remote Nations of the World"] <- 'red'

p <- ggplot(fic, aes(x = date, y = weightedavg)) + geom_point() + geom_smooth(color = 'black', linetype = 'dashed') +
  theme_bw() + 
  scale_y_continuous('', breaks = timebreaks, labels = timelabels) +
  scale_x_continuous('', breaks = c(1719, 1800, 1900, 2000)) +
  theme(text = element_text(size = 22, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) 
tiff("/Users/tunder/Dropbox/active/time/images/fig3weightedavg.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)


