use std::{fs::File, os::fd::AsRawFd, io::Result};
use libc::{O_RDONLY, O_DIRECT, open, read, lseek64, SEEK_SET, c_void, size_t};
use std::ffi::CString;

pub struct DirectLinux { fd: i32, page: usize }

impl DirectLinux {
    pub fn open(path: &str) -> Result<Self> {
        let c = CString::new(path).unwrap();
        let fd = unsafe { open(c.as_ptr(), O_RDONLY | O_DIRECT) };
        if fd < 0 { return Err(std::io::Error::last_os_error()); }
        Ok(Self { fd, page: 4096 })
    }
    fn read_exact_at_inner(&self, off: u64, len: usize) -> Result<Vec<u8>> {
        let mut buf = vec![0u8; ((len + self.page - 1) / self.page) * self.page];
        unsafe { lseek64(self.fd, off as i64, SEEK_SET); }
        let r = unsafe { read(self.fd, buf.as_mut_ptr() as *mut c_void, buf.len() as size_t) };
        if r < 0 { return Err(std::io::Error::last_os_error()); }
        Ok(buf[..len].to_vec())
    }
}

impl Drop for DirectLinux { fn drop(&mut self) { unsafe { libc::close(self.fd); } } }

impl super::DirectReader for DirectLinux {
    fn read_exact_at(&self, offset: u64, len: usize) -> Result<Vec<u8>> { self.read_exact_at_inner(offset, len) }
    fn page_size(&self) -> usize { self.page }
}
