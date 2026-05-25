library(fda)

unitRng = c(0, 1)
bspl2 = create.bspline.basis(unitRng, norder = 2)
plot(bspl2, lwd = 2)

tstFn1 = fd(c(-1, 2), bspl2)
plot(tstFn1)

t = seq(0.1, 0.1)
eval.fd(t, tstFn1)
eval.fd(t, tstFn1, 1)


tstFn2 = fd(c(-1, 3), bspl2)
plot(tstFn2)

par(mfrow = c(3, 1))
fdsumobj = tstFn1 + tstFn2
fddifobj = tstFn1 - tstFn2
fdprdobj = tstFn1 * tstFn2
fdsqrobj = tstFn1 ^ 2

plot(tstFn1, lwd = 2, xlab = "", ylab = "1")
plot(tstFn2, lwd = 2, xlab = "", ylab = "2")
plot(fdsumobj, lwd = 2, xlab = "", ylab = "1+2")

plot(tstFn1, lwd = 2, xlab = "", ylab = "1")
plot(tstFn2, lwd = 2, xlab = "", ylab = "2")
plot(fddifobj, lwd = 2, xlab = "", ylab = "1-2")

plot(tstFn1, lwd = 2, xlab = "", ylab = "1")
plot(tstFn2, lwd = 2, xlab = "", ylab = "2")
plot(fdprdobj, lwd = 2, xlab = "", ylab = "1*2")

plot(tstFn1, lwd = 2, xlab = "", ylab = "1")
plot(tstFn2, lwd = 2, xlab = "", ylab = "2")
plot(fdsqrobj, lwd = 2, xlab = "", ylab = "1^2")



help(daily)

par(mfrow = c(1, 1))
doys = c(182:365, 1:181)
yR = c(0, 365)
tempmat = daily$tempav[doys, ]
tempbasis = create.fourier.basis(yR, 65)

temp.fd = smooth.basis(day.5, tempmat, tempbasis)$fd

temp.fd$fdnames = list("D", "W", "M")

plot(temp.fd, lwd = 2, xlab = 'd', ylab = 'm')














