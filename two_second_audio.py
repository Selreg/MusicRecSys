from pylab import plot, show, figure, imshow 

# %matplotlib inline
import matplotlib.pyplot as plt

import essentia

import essentia.standard
import essentia.streaming

import IPython

#to instantiate an essentia object
loader = essentia.standard.MonoLoader(filename='/home/xelreg/Documents/Capstone/EssentiaTutorial/audio/Disclosure - Latch ft. Sam Smith.wav')



#to process an essentia object
audio = loader()
# print(dir(essentia.standard))

IPython.display.Audio('/home/xelreg/Documents/Capstone/EssentiaTutorial/audio/Disclosure - Latch ft. Sam Smith.wav')

plt.rcParams['figure.figsize'] = (15, 5)
plot(audio[1*44100:2*44100])

plt.title("This is how the 2nd second of this audio looks like:")
plt.show()