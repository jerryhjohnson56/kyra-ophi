// samples/gds_sample.cpp — NVMe->GPU via cuFile (skeleton)
#include <cufile.h>
#include <cuda_runtime.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char** argv) {
  if (argc < 2) { fprintf(stderr, "usage: %s <path>\n", argv[0]); return 1; }
  const char* path = argv[1];
  int fd = open(path, O_RDONLY | O_DIRECT);
  if (fd < 0) { perror("open"); return 2; }

  CUfileDescr_t desc{};
  desc.handle.fd = fd;
  desc.type = CU_FILE_HANDLE_TYPE_OPAQUE_FD;
  CUfileHandle_t cfh;
  if (cuFileHandleRegister(&cfh, &desc) != CU_FILE_SUCCESS) { fprintf(stderr,"cufile reg failed\n"); return 3; }

  void* dptr; size_t bytes = 1<<20; // 1MB
  cudaMalloc(&dptr, bytes);
  ssize_t n = cuFileRead(cfh, dptr, bytes, 0 /*file offset*/, 0 /*device offset*/);
  printf("read %zd bytes to GPU\n", n);

  cuFileHandleDeregister(cfh);
  close(fd);
  cudaFree(dptr);
  return 0;
}
