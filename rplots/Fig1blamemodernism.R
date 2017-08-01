# hypothetical blame it on modernism picture
library(ggplot2)
library(extrafont)
dates = integer(0)
times = numeric(0)
for (i in 1:90) {
  d =  sample(1719:1999, 1)
  t = rnorm(mean = 0.1, sd = 0.9, n = 1)
  if (d < 1922) {
    if (t < -2.4) t = -2.32
  }
  if (d > 1895) {
    modernisteffect = ((d-1895)/33) ^ 2
    if (modernisteffect > 1.65) modernisteffect = 1.65
    t = t - modernisteffect
  }
  dates = c(dates, d)
  times = c(times, t)
}

# add woolf and joyce
dates = c(dates, 1916)
times = c(times, -2.42)
dates = c(dates, 1925)
times = c(times, -2.98)

modernistworld <- data.frame(date = dates, time = times)

timebreaks = c(-2.81, -1.43, 0.365, 1.75, 5.08, 7.650835, 10.65)
timelabels = c('15 min', 'an hour', '6 hours', 'a day', 'a month', 'a year', '20 years')

p <- ggplot(modernistworld, aes(x = date, y = time)) + geom_point() +
  scale_y_continuous("", breaks = timebreaks, labels = timelabels, limits = c(-3.5, 3)) +
  scale_x_continuous('', breaks = c(1719,1800,1900, 2000)) + geom_smooth(se = FALSE, color = 'gray50', linetype = 'dashed') + theme_bw() +
  theme(text = element_text(size = 22, family = "Baskerville"), panel.border = element_blank()) +
  theme(axis.line = element_line(color = 'black')) 

tiff("/Users/tunder/Dropbox/active/time/images/fig1.tiff", height = 6, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)
