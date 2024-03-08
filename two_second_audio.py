from pylab import plot, show, figure, imshow
from essentia.standard import *
import matplotlib.pyplot as plt
import IPython

loader = essentia.standard.MonoLoader(filename='/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/audio/Disclosure - Latch ft. Sam Smith.wav')

# Process the essentia object
audio = loader()

IPython.display.Audio('/home/xelreg/Documents/Capstone/EssentiaTutorial/MusicRecSys/audio/Disclosure - Latch ft. Sam Smith.wav')

plt.rcParams['figure.figsize'] = (15, 6) # set plot sizes to something larger than default

plot(audio[1*44100:2*44100])
plt.title("This is how the 2nd second of this audio looks like:")
show()

w = Windowing(type='hann')
spectrum = Spectrum()
mfcc = MFCC()

frame = audio[6 * 44100: 6 * 44100 + 1024]
spec = spectrum(w(frame))
mfcc_bands, mfcc_coeffs = mfcc(spec)

plot(spec)
plt.title("The spectrum of a frame:")
plt.show()

plot(mfcc_bands)
plt.title("Mel band spectral energies of a frame:")
plt.show()

plot(mfcc_coeffs)
plt.title("First 13 MFCCs of a frame:")
plt.show()

logNorm = UnaryOperator(type='log')
plot(logNorm(mfcc_bands))
plt.title("Log-normalized mel band spectral energies of a frame:")
show()


mfccs = []
melbands = []
melbands_log = []
frameSize = 1024
hopSize = 512

for fstart in range(0, len(audio) - frameSize, hopSize):
    frame = audio[fstart:fstart+frameSize]
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    mfccs.append(mfcc_coeffs)
    melbands.append(mfcc_bands)
    melbands_log.append(logNorm(mfcc_bands))

mfccs = essentia.array(mfccs).T
melbands = essentia.array(melbands).T
melbands_log = essentia.array(melbands_log).T

imshow(melbands[:,:], aspect = 'auto', origin='lower', interpolation='none')
plt.title("Mel band spectral energies in frames")
show()

imshow(melbands_log[:,:], aspect = 'auto', origin='lower', interpolation='none')
plt.title("Log-normalized mel band spectral energies in frames")
show()

imshow(mfccs[1:,:], aspect = 'auto', origin='lower', interpolation='none')
plt.title("MFCCs in frames")
show()

pool = essentia.Pool()

for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512, startFromZero = True):
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    pool.add('lowlevel.mfcc', mfcc_coeffs)
    pool.add('lowlevel.mfcc_bands', mfcc_bands)
    pool.add('lowlevel.mfcc_bands_log', logNorm(mfcc_bands))

imshow(pool['lowlevel.mfcc_bands'].T, aspect = 'auto', origin = 'lower', interpolation = 'none')
plt.title("Mel band spectral energies in frames")
show()

imshow(pool['lowlevel.mfcc_bands_log'].T, aspect = 'auto', origin = 'lower', interpolation = 'none')
plt.title("Log-normalized mel band spectral energies in frame")
show()

imshow(pool['lowlevel.mfcc'].T, aspect = 'auto', origin = 'lower', interpolation = 'none')
plt.title("MFCCs in frames")
show()

# output = YamlOutput(filename = 'mfcc.sig') #use "format = 'json'" for JSON output
# output(pool)

#or as a one-liner:
# YamlOutput(filename = 'mfcc.sig')(pool)

#compute the mean and variance of the frames
aggrPool = PoolAggregator(defaultStats = ['mean', 'stdev'])(pool)

print('Original pool descriptor names:')
print(pool.descriptorNames())
print('')
print('Agrregated pool descriptor names:')
print(aggrPool.descriptorNames())
print('')

YamlOutput(filename = 'mfccaggr.sig')(aggrPool)

