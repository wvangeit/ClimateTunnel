clean:
	rm -rf gifs
	rm -rf data
	rm -rf frames
	mkdir gifs
	mkdir data
	mkdir frames
plot_temp: clean requirements
	curl -o data/GLB.Ts+dSST.csv https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv
	python3 climatetunnel.py
plot_ice: clean requirements
	curl -sL -o data/ice_extent_glb_sii-v3p0_monthly.nc https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/index/sii_v3p0/glb/ice_extent_glb_sii-v3p0_monthly.nc
	curl -sL -o data/ice_area_glb_sii-v3p0_monthly.nc https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/index/sii_v3p0/glb/ice_area_glb_sii-v3p0_monthly.nc
	python3 seaicetunnel.py
plot_co2: clean requirements
	curl -L -o data/co2_mm_gl.txt ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_gl.txt
	python3 co2tunnel.py
requirements:
	python3 -m pip install -qr requirements.txt
plot: clean requirements plot_temp plot_ice
