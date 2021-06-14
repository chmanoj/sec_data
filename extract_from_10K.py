import os
from pathlib import Path
import glob
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

s1_dir = 'downloads/10k_samples'
out_dir = 'downloads/10k_samples_clean'
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

files = glob.glob(s1_dir + '/**/10-k/*.txt', recursive=True)
print(len(files))

failed_files = []

num_files = 0
for sel_file in tqdm(files, desc='Files processed'):
    #txt = Path('downloads/filings/S1/2021/QTR1/27093/0001493152-21-004045.txt').read_text()
    sel_file_path = Path(sel_file)
    try:
        txt = sel_file_path.read_text()
        filing_period_search_term = 'CONFORMED PERIOD OF REPORT'

        filing_period_search_results = [x for x in txt.split('\n')[0:50] if filing_period_search_term in x]

        if len(filing_period_search_results) == 1:
            filing_period = filing_period_search_results[0].split('\t')[-1] + '__' + Path(sel_file).name.replace('.txt', '')
        else:
            filing_period = Path(sel_file).name.replace('.txt', '')

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
            
            # out_file_name = sel_file_path.parent.__str__().split('\\')[-1]
            # out_file_name = out_file_name + '__' + sel_file_path.name
            # out_file_name = os.path.join('\\'.join(sel_file.split('\\')[:-1]), filing_period+'.html')
            out_file_path = os.path.join(Path(sel_file_path.__str__().replace('\\', '/').replace(s1_dir, out_dir)).parent, filing_period+'.html')

            Path(out_file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(out_file_path, "w", encoding='utf-8', errors='ignore') as file:
                file.write(str(soup))

            # with open(os.path.join(out_dir, out_file_name.replace('.txt', '.html')), 'wb') as handle:
            #     handle.write(txt.strip().encode('utf-8', errors='ignore'))
        
        num_files = num_files + 1

        # if num_files >= 2:
        #     break
    except UnicodeDecodeError as e:
        failed_files.append(sel_file)

print(f'Unable to extract data from {len(failed_files)} of {len(files)} files')

