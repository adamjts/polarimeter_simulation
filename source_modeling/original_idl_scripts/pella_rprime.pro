FUNCTION pella_rprime, U
exponent = -0.5*((U-1)/(1.17*U+3.2))^2
RETURN, EXP(exponent)
END
