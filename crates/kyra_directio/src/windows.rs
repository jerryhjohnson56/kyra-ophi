use std::io::Result;
pub struct DirectWin;
impl DirectWin {
    pub fn open(_path: &str) -> Result<Self> {
        // TODO: implement CreateFile(FileFlagNoBuffering) + async reads
        Ok(Self)
    }
}
impl super::DirectReader for DirectWin {
    fn read_exact_at(&self, _offset: u64, _len: usize) -> Result<Vec<u8>> { Ok(vec![]) }
    fn page_size(&self) -> usize { 4096 }
}
