import os
from pathlib import Path
import glob
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

s1_dir = 'downloads/filings/S1/2021'
out_dir = 'downloads/filings/S1/2021_test'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

files = glob.glob(s1_dir + '/**/*.txt', recursive=True)
print(len(files))

for sel_file in tqdm(files, desc='Files processed'):
    #txt = Path('downloads/filings/S1/2021/QTR1/27093/0001493152-21-004045.txt').read_text()
    sel_file_path = Path(sel_file)
    txt = sel_file_path.read_text()
    m = [m for m in re.finditer(r'<html>', txt, flags=re.IGNORECASE)]
    if len(m) > 0:
        start = m[0].span()[0]
    else:
        start = None

    m = [m for m in re.finditer(r'<\/html>', txt, flags=re.IGNORECASE)]
    if len(m) > 0:
        end = m[0].span()[0]
    else:
        end = None

    if start is not None and end is not None:
        html_txt = txt[start:end]
        soup = BeautifulSoup(html_txt)
        txt = soup.text.replace('\n', ' ').replace('\xa0', ' ')
        
        out_file_name = sel_file_path.parent.__str__().split('\\')[-1]
        out_file_name = out_file_name + '__' + sel_file_path.name

        with open(os.path.join(out_dir, out_file_name.replace('.txt', '.rsd.txt')), 'wb') as handle:
            handle.write(txt.strip().encode('utf-8', errors='ignore'))
