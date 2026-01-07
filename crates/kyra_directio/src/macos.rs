use std::{fs::File, os::fd::AsRawFd, io::Result, io::Read};
use libc::{fcntl, F_NOCACHE};

pub struct DirectMac { f: File, page: usize }

impl DirectMac {
    pub fn open(path: &str) -> Result<Self> {
        let f = File::open(path)?;
        unsafe { fcntl(f.as_raw_fd(), F_NOCACHE, 1); }
        Ok(Self { f, page: 4096 })
    }
}
impl super::DirectReader for DirectMac {
    fn read_exact_at(&self, offset: u64, len: usize) -> Result<Vec<u8>> {
        let mut f = &self.f;
        let mut buf = vec![0u8; len];
        // naive; AI should replace with pread or mmap window
        let mut tmp = vec![0u8; offset as usize + len];
        f.read_exact(&mut tmp)?;
        buf.copy_from_slice(&tmp[offset as usize..offset as usize + len]);
        Ok(buf)
    }
    fn page_size(&self) -> usize { self.page }
}
