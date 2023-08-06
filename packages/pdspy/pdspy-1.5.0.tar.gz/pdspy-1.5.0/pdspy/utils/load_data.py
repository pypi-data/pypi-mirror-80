from .. import interferometry as uv
from .. import spectroscopy as sp
from .. import imaging as im
import numpy

def load_data(config, model="disk", gridsize1D=20):

    # Set up the places where we will put all of the data.

    config.visibilities["data"] = []
    config.visibilities["data1d"] = []
    config.visibilities["image"] = []
    config.spectra["data"] = []
    config.spectra["binned"] = []
    config.images["data"] = []

    # Make sure gridsize1D has the proper number of elements.

    if gridsize1D == 20:
        gridsize1D = [20 for i in range(len(config.visibilities["file"]))]

    # Read in the millimeter visibilities.

    for j in range(len(config.visibilities["file"])):
        # Read the raw data.

        data = uv.Visibilities()
        data.read(config.visibilities["file"][j])

        # Center the data. => need to update!

        data = uv.center(data, [config.visibilities["x0"][j], \
                config.visibilities["y0"][j], 1.])

        # Average the data to a more manageable size.

        if model == "disk":
            config.visibilities["data"].append(uv.grid(data, \
                    gridsize=config.visibilities["gridsize"][j], \
                    binsize=config.visibilities["binsize"][j]))
        elif model == "flared":
            config.visibilities["data"].append(data)

        # Scale the weights of the visibilities to force them to be fit well.

        config.visibilities["data"][j].weights *= \
                config.visibilities["weight"][j]

        # Average the visibilities radially.

        if model == "disk":
            config.visibilities["data1d"].append(uv.average(data, \
                    gridsize=gridsize1D[j], radial=True, log=True, \
                    logmin=data.uvdist[numpy.nonzero(data.uvdist)].min()*0.95, \
                    logmax=data.uvdist.max()*1.05))
        elif model == "flared":
            config.visibilities["data1d"].append(uv.average(data, \
                    gridsize=gridsize1D[j], radial=True, log=True, \
                    logmin=data.uvdist[numpy.nonzero(data.uvdist)].min()*0.95, \
                    logmax=data.uvdist.max()*1.05, mode="spectralline"))

        # Read in the image.

        config.visibilities["image"].append(im.readimfits(\
                config.visibilities["image_file"][j]))

    ######################
    # Read in the spectra.
    ######################

    for j in range(len(config.spectra["file"])):
        config.spectra["data"].append(sp.Spectrum())
        config.spectra["data"][j].read(config.spectra["file"][j])

        # Adjust the weight of the SED, as necessary.

        config.spectra["data"][j].unc /= config.spectra["weight"][j]**0.5

        # Merge the SED with the binned Spitzer spectrum.

        if config.spectra["bin?"][j]:
            wave = numpy.linspace(config.spectra["data"][j].wave.min(), \
                    config.spectra["data"][j].wave.max(), \
                    config.spectra["nbins"][j])
            flux = numpy.interp(wave, config.spectra["data"][j].wave, \
                    config.spectra["data"][j].flux)

            good = flux > 0.

            wave = wave[good]
            flux = flux[good]

            config.spectra["binned"].append(sp.Spectrum(wave, flux))
        else:
            config.spectra["binned"].append(config.spectra["data"][j])

        # Merge all the spectra together in one big SED.

        const_unc = 0.1 / config.spectra["weight"][j]**0.5

        try:
            config.spectra["total"].wave = numpy.concatenate((\
                    config.spectra["total"].wave, \
                    config.spectra["binned"][j].wave))
            config.spectra["total"].flux = numpy.concatenate((\
                    config.spectra["total"].flux, \
                    numpy.log10(config.spectra["binned"][j].flux)))
            config.spectra["total"].unc = numpy.concatenate((\
                    config.spectra["total"].unc, \
                    numpy.repeat(const_unc, \
                    config.spectra["binned"][j].wave.size)))

            order = numpy.argsort(config.spectra["total"].wave)

            config.spectra["total"].wave = config.spectra["total"].wave[order]
            config.spectra["total"].flux = config.spectra["total"].flux[order]
            config.spectra["total"].unc = config.spectra["total"].unc[order]
        except:
            config.spectra["total"] = sp.Spectrum(\
                    config.spectra["binned"][j].wave, \
                    numpy.log10(config.spectra["binned"][j].flux), \
                    numpy.repeat(const_unc, \
                    config.spectra["binned"][j].wave.size))

    #####################
    # Read in the images.
    #####################

    for j in range(len(config.images["file"])):
        config.images["data"].append(im.Image())
        config.images["data"][j].read(config.images["file"][j])

    return config.visibilities, config.images, config.spectra
