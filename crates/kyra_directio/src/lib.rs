//! kyra_directio — cross-platform direct I/O skeleton
//! - Linux: io_uring + O_DIRECT
//! - macOS: mmap + fcntl(F_NOCACHE)
//! - Windows: CreateFile(FileFlagNoBuffering)

#[cfg(target_os = "linux")]
mod linux;
#[cfg(target_os = "macos")]
mod macos;
#[cfg(target_os = "windows")]
mod windows;

pub trait DirectReader {
    fn read_exact_at(&self, offset: u64, len: usize) -> std::io::Result<Vec<u8>>;
    fn page_size(&self) -> usize;
}

pub enum DirectFile {
    #[cfg(target_os = "linux")]
    Linux(linux::DirectLinux),
    #[cfg(target_os = "macos")]
    Mac(macos::DirectMac),
    #[cfg(target_os = "windows")]
    Win(windows::DirectWin),
}

impl DirectFile {
    pub fn open(path: &str) -> std::io::Result<Self> {
        #[cfg(target_os = "linux")]
        { Ok(Self::Linux(linux::DirectLinux::open(path)?)) }
        #[cfg(target_os = "macos")]
        { Ok(Self::Mac(macos::DirectMac::open(path)?)) }
        #[cfg(target_os = "windows")]
        { Ok(Self::Win(windows::DirectWin::open(path)?)) }
    }
}
