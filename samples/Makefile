# Makefile for gds_sample (requires NVIDIA CUDA Toolkit & libcufile)
gds_sample: samples/gds_sample.cpp
	$(CXX) -O2 -o $@ $< -lcuda -lcufile
