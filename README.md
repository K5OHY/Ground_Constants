# Ground Constants Estimator

Estimate the HF ground conductivity (σ) and dielectric constant (εr) at any spot in the US, and see what that ground means for your antennas.

Click the map and the page looks up the soil at that point in the USDA soil survey, works out σ and εr for the ground condition and band you pick, and gives you the numbers in the form MMANA-GAL expects. It also compares a vertical with dipoles at different heights over that ground, and takes nearby salt water into account.

**Use it online, nothing to install: [k5ohy.github.io/Ground_Constants](https://k5ohy.github.io/Ground_Constants/)**

> These are estimates from soil survey data, not measurements. Use them as a starting point for modeling. If you can measure your site, enter your own values.

## Contents

- [Quick start](#quick-start)
- [Why not the FCC M3 map?](#why-not-the-fcc-m3-map)
- [Features](#features)
- [How the estimate works](#how-the-estimate-works)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Run it locally](#run-it-locally)
- [Files](#files)
- [Data sources and thanks](#data-sources-and-thanks)

## Quick start

1. Open [the page](https://k5ohy.github.io/Ground_Constants/).
2. Click your operating spot on the map, or type a place name or `lat, lon` and click **Find**.
3. Pick the **ground condition** (Bone dry to Saturated) and the **band**.
4. Read σ and εr from the readout, and click **Copy** to paste them into MMANA-GAL.
5. Scroll down to **What this means for HF antennas** for the vertical vs. dipole comparison.
6. Optional: enter **your dipole height** in feet, or tick **Use my own ground values** if you have measured σ and εr.

## Why not the FCC M3 map?

The FCC M3 ground conductivity map was made from AM broadcast measurements, averaged over tens of miles, at medium frequencies. It gives one number for a whole region. At HF the dielectric constant matters as much as the conductivity, moisture changes both a lot, and the soil at your actual spot can be very different from the regional average. This page works from the soil mapped at the point you click, usually at the scale of a field.

## Features

### Map

- **Click anywhere in the US** to look up the soil there. Search works with place names or coordinates.
- **Map styles:** Light, Dark, Satellite, Street, Topographic, USGS Topo and Shaded relief. No API keys are needed.
- **Soil boundaries** overlay (zoom in close) shows the USDA soil map units.
- **Nearby data** used for an estimate shows as blue dots, and the nearest salt water as a dashed line.

### Readout

- **σ in mS/m and εr**, with a ground class (Very poor to Very good / saline) and the estimated skin depth on the chosen band.
- **MMANA-GAL line** with a Copy button.
- **Data line** showing where the numbers came from: how much of the map unit has lab data, which soil properties were filled with defaults, and whether nearby spots supplied the data.
- **Water:** map units of water are treated as fresh or salt depending on the coastline, and you can switch between them.

### Ground condition and band

- Five moisture settings: Bone dry, Dry, Moist, Wet, Saturated.
- Bands from 160m to 6m. The band changes how deep into the ground the estimate reaches and the antenna comparison.
- A table shows all five moisture settings side by side, so you can see how much rain changes your site.

### What this means for HF antennas

- **Verdict** naming the antenna, for example "35 ft dipole favored broadside" or "Vertical ≈ 30 ft dipole".
- **Flat-ground comparison** in dBi at 5°, 10° and 20° for a ground-mounted ¼λ vertical, a dipole at ¼λ, a dipole at ½λ, and your own dipole height if you enter one.
- **Notes** on verticals (pseudo-Brewster angle, radials), horizontals (height), low dipoles and NVIS on 40m and below, moisture, skin depth and salt water.

### Salt water

The page carries its own copy of the US coastline. After each lookup it finds the nearest salt water and estimates how much of the ground where the signal reflects lies over the sea, for each antenna and angle. When the sea makes a difference, buttons let you compare **toward salt water** with **inland**. This is where a seaside vertical gets its advantage.

### Your own values

- **Your dipole height** adds a row to the table and becomes the dipole the verdict compares against. It is remembered in your browser.
- **Use my own ground values** replaces the estimate with your measured σ and εr in the readout and the antenna comparison. It works without clicking a location.

### Manual soil type

Pick a soil texture and salinity (or fresh or salt water) to see typical values, for what-if comparisons or when the soil service is down.

## How the estimate works

1. **Soil data.** The clicked point is sent to USDA NRCS Soil Data Access (SSURGO). It returns the soil map unit, its component soils and their share, and each soil's layers down to about 2 m: sand and clay, bulk density, water held at field capacity and wilting point, salinity (EC) and cation exchange capacity (CEC).
2. **Moisture.** Each ground condition sets the water content of every layer, from 40% of the wilting point (Bone dry) to 90% of the pore space (Saturated).
3. **Dielectric constant.** CRIM mixing of mineral grains, water and air.
4. **Conductivity.** An Archie-type model: pore-water conductivity from the salinity, a porosity and water-content factor, plus a surface-conduction term from clay.
5. **Depth weighting.** Layers are weighted by how much of the radio field reaches them on the chosen band. Rock layers (only where the survey says bedrock or cemented) are treated as limestone or caliche; organic layers (muck, peat) get organic-soil values.
6. **Missing data.** Where there is no soil data (urban land, pits, unsurveyed areas), the page averages the nearest real soil data, searching outward up to about 37 miles and weighting the closest most.
7. **Antenna comparison.** Each antenna's free-space pattern combined with the reflection off flat ground with these constants, with salt water blended in where it lies in the reflection zone.

The full details are in **How the estimate works** at the bottom of the page.

## Limitations

- **Not validated.** The estimates have not been checked against HF ground measurements. Treat them as a starting point. For real numbers, measure your site with a VNA ground probe (see [N6LF's work](https://www.antennasbyn6lf.com)) and use **Use my own ground values**.
- **No frequency dependence in the soil model.** Each layer's σ and εr are the same on every band; only the depth weighting and reflection change. Real soils vary somewhat with frequency.
- **Flat ground.** The antenna comparison ignores hills, slopes, buildings and trees.
- **Radials.** The vertical assumes a good radial system; loss in the ground near the antenna is not included.
- **Salt water model** is simplified, and the coastline covers ocean and bays only (not the Great Lakes or inland salt lakes).
- **Soil survey data** is mapped at field scale and describes typical soil, not your exact spot. Fill, caliche layers or a damp low spot can differ.

## Troubleshooting

- **"Could not reach the USDA soil service".** The USDA server is occasionally slow or down. Try again in a few minutes, or use **Manual soil type**.
- **Soil boundaries don't show.** Zoom in close (street level). If the panel says the USDA map server isn't responding, the overlay is unavailable for now; lookups still work.
- **A spot shows "Low coverage".** Most of that map unit has no soil data (often urban land). Try a spot nearby, or treat the result as rough.
- **Place search finds nothing.** Try a town or park name, or enter coordinates as `lat, lon`.

## Run it locally

Download `index.html` and open it in a web browser. There is nothing to install. It needs an internet connection for the soil data and map tiles.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: page, code and the embedded US coastline data |
| `build_coastline.py` | Rebuilds the embedded coastline data from the OpenStreetMap source |
| `LICENSE` | MIT license for the code, plus the terms for the data |

## Data sources and thanks

- [USDA NRCS Soil Data Access](https://sdmdataaccess.nrcs.usda.gov/) (SSURGO): soil data and soil map overlay
- Coastline: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL), via [geo-maps](https://github.com/simonepri/geo-maps)
- Map tiles: Esri, USGS The National Map
- Place search: Esri World Geocoder, with OpenStreetMap Nominatim as a fallback
- Built with [Leaflet](https://leafletjs.com/)
- Ground measurement background: [Rudy Severns, N6LF](https://www.antennasbyn6lf.com)

## License

MIT License for the code. See [LICENSE](LICENSE) for the data terms.
