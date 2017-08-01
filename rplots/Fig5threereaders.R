library(ggplot2)
library(dplyr)
times <- read.csv('/Users/tunder/Dropbox/python/time/averagetimes.csv')
fic <- filter(times, col != 'red')
timebreaks = c(-4.82, -2.81, -1.43, 0.365, 1.75, 3.7, 5.08, 7.650835, 10.65)
timelabels = c('2 min', '15 min', 'an hour', '6 hours', 'a day', 'a week', 'a month', 'a year', '20 years')
fic$col <- as.character(fic$col)
fic$col[fic$col == 'black'] <- 'Underwood'
fic$col[fic$col == 'green'] <- 'Lee'
fic$col[fic$col == 'blue'] <- 'Mercado'

p <- ggplot(fic, aes(x = date, y = weightedavg, linetype = col, color = col, shape = col)) + geom_point() + 
  geom_smooth(se = FALSE, show.legend = FALSE) + theme_bw() + 
  scale_linetype_manual(guide = 'none', values = c('solid','dashed', 'solid')) + 
  scale_color_manual(name = 'reader\n', values = c('black', 'black', 'gray60')) +
  scale_shape_manual(name = 'reader\n', values = c(16, 2, 16)) +
  scale_y_continuous('', breaks = timebreaks, labels = timelabels) +
  scale_x_continuous('', breaks = c(1719, 1800, 1900, 2000)) +
  theme(text = element_text(size = 22, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) 
tiff("/Users/tunder/Dropbox/active/time/images/fig4threereaders.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)

mercadomodel <- loess(fic$weightedavg[fic$col == 'Mercado'] ~ fic$date[fic$col == 'Mercado'], surface = 'direct')
leemodel <- loess(fic$weightedavg[fic$col == 'Lee'] ~ fic$date[fic$col == 'Lee'], surface = 'direct')
underwoodmodel <- loess(fic$weightedavg[fic$col == 'Underwood'] ~ fic$date[fic$col == 'Underwood'], surface = 'direct')

mercado <- predict(mercadomodel, newdata = seq(1719, 1999))
lee <- predict(leemodel, newdata = seq(1719, 1999))
underwood <- predict(underwoodmodel, newdata = seq(1719, 1999))
print(cor(mercado, underwood))
print(cor(underwood, lee))
print(cor(lee, mercado))