# Ground Constants Estimator

Estimate the HF ground conductivity (σ) and dielectric constant (εr) at any spot in the world, and see what that ground means for your antennas.

Click the map and the page looks up the soil at that point (in the USDA soil survey in the US, or in ISRIC's SoilGrids global data elsewhere), works out σ and εr for the ground condition and band you pick, and gives you the numbers in the form MMANA-GAL expects. It also compares a vertical with dipoles at different heights over that ground, and takes nearby salt water into account.

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
2. Click your operating spot on the map, type a place name or `lat, lon` and click **Find**, or click **Use my location** and allow location access in your browser.
3. Pick the **ground condition** (Bone dry to Saturated) and the **band**.
4. Read σ and εr from the readout, and click **Copy** to paste them into MMANA-GAL.
5. Scroll down to **What this means for HF antennas** for the vertical vs. dipole comparison.
6. Optional: enter **your dipole height** in feet, or tick **Use my own ground values** if you have measured σ and εr.

## Why not the FCC M3 map?

The FCC M3 ground conductivity map was made from AM broadcast measurements, averaged over tens of miles, at medium frequencies. It gives one number for a whole region. At HF the dielectric constant matters as much as the conductivity, moisture changes both a lot, and the soil at your actual spot can be very different from the regional average. This page works from the soil mapped at the point you click, usually at the scale of a field.

## Features

### Map

- **Click anywhere in the world** to look up the soil there. Search works with place names or coordinates.
- **Use my location** centers the map on your current browser location and looks up the soil there. Use the panel button or the target icon beneath the map's +/− zoom buttons. Location access is requested only when you click either control.
- **Map styles:** Light, Dark, Satellite, Street, Topographic, USGS Topo and Shaded relief. No API keys are needed.
- **Soil boundaries** overlay (zoom in close) shows the USDA soil map units.
- **Nearby data** used for an estimate shows as blue dots, and the nearest salt water as a dashed line.

### Readout

- **σ in mS/m and εr**, with a ground class (Very poor to Very good / saline) and the estimated skin depth on the chosen band.
- **MMANA-GAL line** with a Copy button.
- **Data line** showing where the numbers came from: how much of the map unit has lab data, which soil properties were filled with defaults, and whether nearby spots supplied the data.
- **Source:** the data line names where the numbers came from: the USDA survey, nearby USDA soils, or SoilGrids global data.
- **Water:** map units of water are treated as fresh or salt depending on the coastline, and you can switch between them.

### Ground condition and band

- Five moisture settings: Bone dry, Dry, Moist, Wet, Saturated.
- Bands from 160m to 6m. The band changes how deep into the ground the estimate reaches and the antenna comparison.
- A table shows all five moisture settings side by side, so you can see how much rain changes your site.

### What this means for HF antennas

- **Verdict** naming the antenna, with a line saying whether it holds from bone dry to saturated ground, for example "35 ft dipole favored broadside" or "Vertical ≈ 30 ft dipole".
- **Illustrative flat-ground comparison** in dBi at 5°, 10° and 20° for a ground-mounted ¼λ vertical, a dipole at ¼λ, a dipole at ½λ, and your own dipole height if you enter one.
- **Notes** on verticals (pseudo-Brewster angle, radials), horizontals (height), low dipoles and NVIS on 40m and below, moisture, skin depth and salt water.

### Salt water

The page uses the OpenStreetMap coastline for the whole world, loaded in tiles for the area around the spot you click (a US-only copy is built in for when the page is opened as a file). After each lookup it finds the nearest salt water and estimates how much of the ground where the signal reflects lies over the sea, for each antenna and angle. When the sea makes a difference, buttons let you compare **toward salt water** with **inland**. This is where a seaside vertical gets its advantage.

### Your own values

- **Your dipole height** adds a row to the table and becomes the dipole the verdict compares against. It is remembered in your browser.
- **Use my own ground values** replaces the estimate with your measured σ and εr in the readout and the antenna comparison. It works without clicking a location.

### Manual soil type

Pick a soil texture and salinity (or fresh or salt water) to see typical values, for what-if comparisons or when the soil service is down.

## How the estimate works

1. **Choosing a source.** In the US the page asks the USDA soil survey first. Outside the US, where USDA has no data, or when the USDA service is down, it uses [SoilGrids](https://soilgrids.org) from ISRIC, a worldwide soil grid of about 250 m. Open sea is recognized from the coastline.
2. **USDA soil data.** The clicked point is sent to USDA NRCS Soil Data Access (SSURGO). It returns the soil map unit, its component soils and their share, and each soil's layers down to about 2 m: sand and clay, bulk density, water held at field capacity and wilting point, salinity (EC) and cation exchange capacity (CEC).
3. **Moisture.** Each ground condition sets the water content of every layer, from 40% of the wilting point (Bone dry) to 90% of the pore space (Saturated).
4. **Dielectric constant.** CRIM mixing of mineral grains, water and air.
5. **Conductivity.** An Archie-type model: pore-water conductivity from the salinity, a porosity and water-content factor, plus a surface-conduction term from clay.
6. **Depth weighting.** Layers are weighted by how much of the radio field reaches them on the chosen band. Rock layers (only where the survey says bedrock or cemented) are treated as limestone or caliche; organic layers (muck, peat) get organic-soil values.
7. **Missing data.** Where there is no soil data (urban land, pits, unsurveyed areas), the page averages the nearest real soil data, searching outward up to about 37 miles and weighting the closest most.
8. **Antenna comparison.** Each antenna's free-space pattern combined with the reflection off flat ground with these constants, with salt water blended in where it lies in the reflection zone. Dipole gains are corrected for how radiation resistance changes with height (image theory). The verdict is recomputed for all five ground conditions to show whether it depends on moisture.

The full details are in **How the estimate works** at the bottom of the page.

## Limitations

- **Not validated.** The estimates have not been checked against HF ground measurements. Treat them as a starting point. For real numbers, measure your site with a VNA ground probe (see [N6LF's work](https://www.antennasbyn6lf.com)) and use **Use my own ground values**.
- **No frequency dependence in the soil model.** Each layer's σ and εr are the same on every band; only the depth weighting and reflection change. Real soils vary somewhat with frequency.
- **The antenna comparison is illustrative.** It combines ideal patterns with ground reflection; it does not compute antenna currents, feedpoint impedance, radial losses or terrain. Use it to pick ground values to try, then model your antenna in MMANA-GAL or NEC.
- **Deep ground is assumed.** Soil data stops at about 2 m; below that the deepest layer is assumed to continue. On dry ground and low bands most of the estimate can come from that assumption, and the page warns when it does.
- **Conductivity from salinity is modeled.** USDA's EC is measured on a saturated soil-paste extract; turning it into bulk HF conductivity uses an uncalibrated model, and the clay surface-conduction term can dominate on non-saline ground.
- **Radials.** The vertical assumes a good radial system; loss in the ground near the antenna is not included.
- **Global data is coarser.** SoilGrids is predicted by computer on a grid of about 250 m rather than mapped in the field, and it has no salinity data, so it assumes non-saline soil. Near the sea or on salty desert ground, use **Manual soil type** with a salinity setting to see the difference. A global lookup reads 36 map layers from ISRIC's map server and takes a few seconds. In towns, where SoilGrids has no value, the soil around the spot is averaged.
- **Salt water model** is simplified, and the coastline covers oceans and bays only (not lakes, including the Great Lakes and inland salt lakes). Near the 180° meridian (Fiji, western Aleutians) coastline across the line is not used. Opened as a file rather than from the website, only the US coastline is available.
- **Soil survey data** is mapped at field scale and describes typical soil, not your exact spot. Fill, caliche layers or a damp low spot can differ.

## Troubleshooting

- **"The USDA soil service didn't answer".** The USDA server is occasionally slow or down for updates. The page switches to SoilGrids global data in the meantime; try again later for the detailed USDA data.
- **A global lookup is slow.** It loads 36 small map layers from ISRIC; the status line counts them. Spots you have already looked up are remembered and load instantly.
- **Soil boundaries don't show.** Zoom in close (street level). If the panel says the USDA map server isn't responding, the overlay is unavailable for now; lookups still work.
- **A spot shows "Low coverage".** Most of that map unit has no soil data (often urban land). Try a spot nearby, or treat the result as rough.
- **Place search finds nothing.** Try a town or park name, or enter coordinates as `lat, lon`.
- **Current location is unavailable.** Allow location access in your browser and device settings, then try again. You can always click the map or search instead. Outside the US the page uses SoilGrids global data.

## Run it locally

Download `index.html` and open it in a web browser. There is nothing to install. It needs an internet connection for the soil data and map tiles.

Current location requires a secure browser context. If it is unavailable when opening the file directly, serve this folder on localhost (for example, `python3 -m http.server`) and open `http://localhost:8000`.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole app: page, code and the built-in US coastline |
| `coast/` | Worldwide coastline in 30° tiles, loaded as needed |
| `build_coastline.py` | Rebuilds the built-in US coastline and the `coast/` tiles from the OpenStreetMap source |
| `LICENSE` | MIT license for the code, plus the terms for the data |

## Data sources and thanks

- [USDA NRCS Soil Data Access](https://sdmdataaccess.nrcs.usda.gov/) (SSURGO): US soil data and soil map overlay
- [SoilGrids](https://soilgrids.org) © ISRIC – World Soil Information, CC BY 4.0: global soil data
- Coastline: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors (ODbL), via [geo-maps](https://github.com/simonepri/geo-maps)
- Map tiles: Esri, USGS The National Map
- Place search: Esri World Geocoder, with OpenStreetMap Nominatim as a fallback
- Built with [Leaflet](https://leafletjs.com/)
- Ground measurement background: [Rudy Severns, N6LF](https://www.antennasbyn6lf.com)

## License

MIT License for the code. See [LICENSE](LICENSE) for the data terms.
