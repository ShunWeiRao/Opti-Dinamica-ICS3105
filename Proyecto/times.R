library(MASS)
library(readxl)
X180 <- read_excel("~/Downloads/180.xlsx")
X180_2 <- read_excel("~/Downloads/180_2.xlsx")
X180_5 <- read_excel("~/Downloads/180_5.xlsx")
X180_6 <- read_excel("~/Downloads/180_5.xlsx", 
                     sheet = "Hoja2")
cumul = hist(X180$dif, probability = TRUE, main = "Tiempo estimado",
             xlab = "tiempo", ylab = "Prob")
cumul_2 = hist(X180_2$dif, probability = TRUE, main = "Tiempo estimado",
             xlab = "tiempo", ylab = "Prob")
cumul_5 = hist(X180_5$dif, probability = TRUE, main = "Tiempo estimado",
             xlab = "tiempo", ylab = "Prob")
cumul_6 = hist(X180_6$dif, probability = TRUE, main = "Tiempo estimado",
               xlab = "tiempo", ylab = "Prob",)
mu = mean(X180$dif)
sigma = sd(X180$dif)
curve(dnorm(x, mu, sigma^2),add = TRUE)


curve(dgamma(x, (9.5/5)^2, 9.5/5^2), add = TRUE)

rgamma(1,(9.5/1)^2, 9.5/1^2)



ks.test(X180$dif, pnorm, mu, sigma^2)

