clean:
	rm -rf gifs
	rm -rf data
	mkdir gifs
	mkdir data
	mkdir frames
plot_temp: clean
	curl -o data/GLB.Ts+dSST.csv https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv
	python climatetunnel.py
plot_ice: clean
	curl -L -o data/nsidc_global_nt_final_and_nrt.txt.gz https://sites.google.com/site/arctischepinguin/home/sea-ice-extent-area/data/nsidc_global_nt_final_and_nrt.txt.gz?attredirects=0
	gunzip -f data/nsidc_global_nt_final_and_nrt.txt.gz
	python seaicetunnel.py
plot_co2: clean
	curl -L -o data/co2_mm_gl.txt ftp://ftp.cmdl.noaa.gov/products/trends/co2/co2_mm_gl.txt
	python co2tunnel.py
requirements:
	pip install -r requirements.txt
plot: clean requirements plot_temp plot_ice
