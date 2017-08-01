# plot density distribution
library(ggplot2)
library(ggjoy)
library(dplyr)
timebreaks = c(-4.82, -1.43, 1.75, 5.08, 10.65)
timelabels = c('2 min', 'hour', 'day', 'month', '20 years')
segs <- read.csv('/Users/tunder/Dropbox/python/time/segleveldata.csv')
segs$col = as.character(segs$col)
ficsegs <- filter(segs, col != 'red')

ficsegs$col[ficsegs$date < 1800] = '18c'
ficsegs$col[ficsegs$date < 1900 & ficsegs$date > 1799] = '19c'
ficsegs$col[ficsegs$date < 3000 & ficsegs$date > 1899] = '20c'

p <- ggplot(ficsegs, aes(x = time, y = col)) + geom_joy(alpha = 0.8) +
  scale_x_continuous("", breaks = timebreaks, labels = timelabels, limits = c(-8,15)) +
  scale_y_discrete('') + theme_joy() +
  theme(text = element_text(size = 32, family = 'Baskerville')) +
  # ggtitle('Time narrated in 250-word passages of fiction\n') +
  theme(plot.title = element_text(size = 22),
        axis.text.x = element_text(size = 18),
        axis.text.y = element_text(size = 18))
plot(p)
tiff("/Users/tunder/Dropbox/active/time/images/fig5ggjoy.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
