# Plot functions
#
#
# Copyright (c) 2016 Alfredo Mungo <alfredo.mungo@openmailbox.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# f: function f(w) to plot
# w: the frequency (rad/s) values to plot f for
# phicorr: phase correction
#  - none: no phase correction
#  - n: negative correction (phase will be always <= 0)
#  - p: positive correction (phase will be always >= 0)
#  - auto: automatic correction
plot.bode <- function(f, w, phicorr='auto') {
  dev.new()
  close.screen(close.screen())
  scr = split.screen(c(2, 1), erase=T)

  y = f(w)

  # Magnitude
  screen(scr[1])
  plot(w, 20*log10(abs(y)), type='l', xlab='', ylab='Magnitude', log='x')
  grid(col='black')
  title("Bode plot")

  # Phase
  screen(scr[2])
  phi=180/pi*Arg(y)

  if(phicorr == 'n') {
    for(i in 1:length(phi)) {
      phi[i] = if (phi[i] <= 0) phi[i] else (phi[i] - 360)
    }
  } else if(phicorr == 'p') {
    for(i in 1:length(phi)) {
      phi[i] = if (phi[i] >= 0) phi[i] else (phi[i] + 360)
    }
  } else if(phicorr == 'auto') {
    phi = phase.autocorrect(phi)
  }

  plot(w, phi, type='l', xlab=expression(omega), ylab='Phase', log='x')
  grid(col='black')
}

plot.polar <- function(f, w) {
  dev.new()
  close.screen(close.screen())

  plot(f(w), type='l')
  title('Polar plot')
  grid(col='black')
}

plot.nyquist <- function(f, w) {
  dev.new()
  close.screen(close.screen())

  y=c(f(w), rev(f(-w)))

  plot(y, type='n')
  usr = par('usr')
  xlim = c(usr[1:2])
  ylim = c(usr[3:4])

  plot(y, type='l', xlim=xlim, ylim=ylim)
  par(new=T, fg='red')
  plot(-1+0i, type='p', ylab='', xlab='', xlim=xlim, ylim=ylim, axes=F)
  title('Nyquist plot')
  grid(col='black')
}

plot.nichols <- function(f, w, phicorr='auto') {
  dev.new()
  close.screen(close.screen())

  y=f(w)
  mag=20*log10(abs(y))
  phi=180/pi*Arg(y)

  if(phicorr == 'n') {
    for(i in 1:length(phi)) {
      phi[i] = if (phi[i] <= 0) phi[i] else (phi[i] - 360)
    }
  } else if(phicorr == 'p') {
    for(i in 1:length(phi)) {
      phi[i] = if (phi[i] >= 0) phi[i] else (phi[i] + 360)
    }
  } else if(phicorr == 'auto') {
    phi = phase.autocorrect(phi)
  }

  plot(phi, mag, type='l', xlab='Phase', ylab='Magnitude')
  title('Nichols plot')
  grid(col='black')
}


# Returns the index of the first value 0 with tolerance or NULL if not found
find.zero <- function(arr, tol = .Machine$double.eps ^ 0.5) {
  for(i in 1:length(arr)) {
    if(abs(arr[i]) < tol)
      return(i)
  }

  return(NULL)
}

# Returns the index of the first jump in a vector with distance of at least tol
find.jump <- function(arr, tol = 1) {
  for(i in 2:length(arr)) {
    if(abs(arr[i] - arr[i-1]) >= tol) { # Jump here
      return(i)
    }
  }

  return(NULL)
}

phase.autocorrect <- function(phi) {
  idx = find.jump(phi, 355)

  if(is.null(idx)) # Didn't find suitable jump, return input as is
    return(phi)

  if((phi[idx] - phi[idx-1]) > 0) { # Phase is going up
    return(c(phi[1:(idx-1)], phi[idx:length(phi)] - 360))
  } else { # Phase is going down
    return(c(phi[1:(idx-1)], phi[idx:length(phi)] + 360))
  }
}
