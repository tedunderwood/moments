# Make unweighted meantime graph
library(ggplot2)
library(dplyr)
times <- read.csv('/Users/tunder/Dropbox/python/time/averagetimes.csv')
# fic <- filter(times, col != 'red')
timebreaks = c(-4.82, -2.81, -1.43, 0.365, 1.75, 3.7, 5.08, 7.650835, 10.65)
timelabels = c('2 min', '15 min', 'an hour', '6 hours', 'a day', 'a week', 'a month', 'a year', '20 years')
times$col <- as.character(times$col)
times$col[times$col != 'red'] <- '\nfiction'
times$col[times$col == 'red'] <- '\nbiography and\nautobiography'

p <- ggplot(times, aes(x = meanhard, y = meantime, shape = col)) + geom_point() + 
  theme_bw() + 
  scale_y_continuous('', breaks = timebreaks, labels = timelabels) +
  scale_x_continuous('\nratio of words in Stanford "concrete" list to all words') +
  scale_shape_manual(name = 'genre', values = c(2, 16)) +
  theme(text = element_text(size = 18, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) 
tiff("/Users/tunder/Dropbox/active/time/images/fig7hardseeds.tiff", height = 5.5, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
