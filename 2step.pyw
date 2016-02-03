#!/usr/bin/env python3

'''
Second order system step response parameter calculator and plotter.

This program is aimed at calculating a set of parameters for the response of
a second order system with complex conjugate poles and no zeros.


Copyright (c) 2016 Alfredo Mungo <alfredo.mungo@openmailbox.org>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import math
import tkinter as tk
#import tkinter.ttk as ttk

def compute(var, dummy, op):
  try:
    mu = v_gain.get()
    f = v_freq.get()
    xi = v_damp.get()

    if xi < 0.02: # Avoid freezing
      txt_damp['fg'] = 'red'
      return
    else:
      txt_damp['fg'] = txt_damp_fg_orig

    yinf = mu
    tmax = math.pi/f/math.sqrt(1-xi**2)
    ymax = mu*(1+math.exp(-xi*math.pi/math.sqrt(1-xi**2)))
    sperc = 100*(ymax-yinf)/yinf
    ta1 = 4.6/xi/f
    N = 1/2/xi

    v_yinf.set(yinf)
    v_tmax.set(tmax)
    v_ymax.set(ymax)
    v_sperc.set(sperc)
    v_ta1.set(ta1)
    v_nosc.set(N)

    plot(ta1, 0.1/f*xi, mu, f, xi, ymax, tmax)
  except Exception as e:
    pass

def plot(ta1, inc, mu, wn, xi, ymax, tmax):
  cvasw = cvas.winfo_width()
  cvash = cvas.winfo_height()
  response = []
  tmax_plot = ta1 * 1.1

  for t, y in step_response(tmax_plot, inc, mu, wn, xi):
    t = t / tmax_plot * cvasw
    y = (-y / ymax * 1.3 + 1.5) * cvash/2

    response.append(t)
    response.append(y)

  cvas.delete('all')

  # Plot parameters
  cvas.create_line(0, (-mu * 1.3 / ymax + 1.5) * cvash / 2, cvasw, (-mu * 1.3 / ymax + 1.5) * cvash/2, fill='grey', dash='.') # yinf
  cvas.create_line(tmax/tmax_plot * cvasw, 0, tmax/tmax_plot * cvasw, cvash, fill='black', dash='.') # tmax

  # Plot response
  cvas.create_line(*response, fill='red', smooth='true')
  
def step_response(tmax, inc, mu, wn, xi):
  """
    tmax: time after which to stop generating the response
    inc: time increment
    wn: natural frequency
    xi: damping factor
  """
  y = lambda t: mu * (1 - math.exp(-xi*wn*t)/math.sqrt(1-xi**2)*math.sin(wn*t*math.sqrt(1-xi**2) + math.acos(xi)))
  t = 0

  while t < tmax:
    yield (t, y(t))
    t += inc

root = tk.Tk()
root.title('2nd order system step response')
root.wm_resizable(0, 0)

frame = tk.Frame(padx=4, pady=4)
iframe = tk.LabelFrame(frame, text='Input data')
iiframe = tk.Frame(iframe)

v_gain = tk.DoubleVar(name='mu')
v_gain.trace('w', compute)
lbl_gain = tk.Label(iiframe, text='mu', anchor='e')
txt_gain = tk.Entry(iiframe, textvariable=v_gain, takefocus=1)
lbl_gain.grid(sticky='e')
txt_gain.grid(column=1, row=0, padx=(2, 16))
txt_gain.focus()
txt_gain.selection_range(0, len(str(v_gain.get())))

v_freq = tk.DoubleVar(name='f')
v_freq.trace('w', compute)
lbl_freq = tk.Label(iiframe, text='Wn')
txt_freq = tk.Entry(iiframe, textvariable=v_freq)
lbl_freq.grid(column=2, row=0)
txt_freq.grid(column=3, row=0, padx=(2, 16))

v_damp = tk.DoubleVar(name='xi')
v_damp.trace('w', compute)
lbl_damp = tk.Label(iiframe, text='Xi')
txt_damp = tk.Entry(iiframe, textvariable=v_damp)
lbl_damp.grid(column=4, row=0)
txt_damp.grid(column=5, row=0, padx=(2, 8))
txt_damp_fg_orig = txt_damp['fg']

iiframe.pack()
iframe.grid(column=0, row=0, columnspan=3, sticky='we')

oframe = tk.LabelFrame(frame, text='Output')

v_yinf = tk.DoubleVar()
lbl_yinf = tk.Label(oframe, text='yinf')
txt_yinf = tk.Entry(oframe, textvariable=v_yinf, state='readonly')
lbl_yinf.grid(column=0, row=0)
txt_yinf.grid(column=1, row=0, padx=(2, 16))

v_tmax = tk.DoubleVar()
lbl_tmax = tk.Label(oframe, text='Tmax')
txt_tmax = tk.Entry(oframe, textvariable=v_tmax, state='readonly')
lbl_tmax.grid(column=0, row=1)
txt_tmax.grid(column=1, row=1, padx=(2, 16))

v_ymax = tk.DoubleVar()
lbl_ymax = tk.Label(oframe, text='ymax')
txt_ymax = tk.Entry(oframe, textvariable=v_ymax, state='readonly')
lbl_ymax.grid(column=0, row=2)
txt_ymax.grid(column=1, row=2, padx=(2, 16))

v_sperc = tk.DoubleVar()
lbl_sperc = tk.Label(oframe, text='S%')
txt_sperc = tk.Entry(oframe, textvariable=v_sperc, state='readonly')
lbl_sperc.grid(column=0, row=3)
txt_sperc.grid(column=1, row=3, padx=(2, 16))

v_ta1 = tk.DoubleVar()
lbl_ta1 = tk.Label(oframe, text='T1%')
txt_ta1 = tk.Entry(oframe, textvariable=v_ta1, state='readonly')
lbl_ta1.grid(column=0, row=4)
txt_ta1.grid(column=1, row=4, padx=(2, 16))

v_nosc = tk.DoubleVar()
lbl_nosc = tk.Label(oframe, text='No')
txt_nosc = tk.Entry(oframe, textvariable=v_nosc, state='readonly')
lbl_nosc.grid(column=0, row=5)
txt_nosc.grid(column=1, row=5, padx=(2, 16))

oframe.grid(column=0, row=1, sticky='ns')

cvas = tk.Canvas(frame, bg='white')
cvas.grid(column=1, row=1, rowspan=1, columnspan=2, sticky='nswe')

frame.pack()

root.mainloop()
