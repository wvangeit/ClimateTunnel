clean:
	rm -rf gifs
	rm -rf data
	rm -rf frames
	mkdir gifs
	mkdir data
	mkdir frames
plot_temp: clean
	curl -o data/GLB.Ts+dSST.csv https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv
	python climatetunnel.py
plot_ice: clean
	curl -sL -o data/osisaf_glb_sie_monthly.nc https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/index/v2p2/glb/osisaf_glb_sie_monthly.nc
	curl -sL -o data/osisaf_glb_sia_monthly.nc https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/index/v2p2/glb/osisaf_glb_sia_monthly.nc
	python seaicetunnel.py
plot_co2: clean
	curl -L -o data/co2_mm_gl.txt ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_gl.txt
	python co2tunnel.py
requirements:
	pip install -qr requirements.txt
plot: clean requirements plot_temp plot_ice
