clean:
	rm -rf gifs
	rm -rf data/GLB.Ts+dSST.csv
	mkdir gifs
plot_temp:
	curl -o data/GLB.Ts+dSST.csv https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv
	python climatetunnel.py
plot_ice:
	curl -L -o data/nsidc_global_nt_final_and_nrt.txt.gz https://sites.google.com/site/arctischepinguin/home/sea-ice-extent-area/data/nsidc_global_nt_final_and_nrt.txt.gz?attredirects=0
	gunzip -f data/nsidc_global_nt_final_and_nrt.txt.gz
	python seaicetunnel.py
requirements:
	pip install -r requirements.txt
plot: clean requirements plot_temp plot_ice
