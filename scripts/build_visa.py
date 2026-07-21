import json
d=json.load(open('visa_agg.json'))

OVERRIDE={
 'China, Peoples Republic of (excl SARs)':'China','Korea, South':'South Korea','Korea, North':'North Korea',
 'Hong Kong (SAR of China)':'Hong Kong','Taiwan':'Taiwan','Viet Nam':'Vietnam',
 'United States of America':'United States','United Kingdom, Channel Islands and Isle of Man':'United Kingdom',
 'Iran, Islamic Republic of':'Iran','Russian Federation':'Russia','Syrian Arab Republic':'Syria',
 'Lao Peoples Democratic Republic':'Laos','Tanzania, United Republic of':'Tanzania',
 'Macau (SAR of China)':'Macau','Myanmar (Burma)':'Myanmar','Brunei Darussalam':'Brunei',
 'Bolivia, Plurinational State of':'Bolivia','Venezuela, Bolivarian Republic of':'Venezuela',
 'Congo, Democratic Republic of the':'DR Congo','Moldova, Republic of':'Moldova','Not Recorded':'Not recorded'
}
def clean(name):
    if name in OVERRIDE: return OVERRIDE[name]
    n=name
    for junk in [' (excl SARs)',' (SAR of China)']:
        n=n.replace(junk,'')
    return n.strip()

def cleanmap(fydict):
    out={}
    for fy,cd in fydict.items():
        o={}
        for c,v in cd.items(): o[clean(c)]=o.get(clean(c),0)+v
        out[fy]=o
    return out

byFYcty=cleanmap(d['byFYcty'])
ctySec={}
for c,secd in d['ctySec_latest'].items():
    cc=clean(c)
    e=ctySec.setdefault(cc,{})
    for s,v in secd.items(): e[s]=e.get(s,0)+v

SECTORS=['Higher Education','VET','ELICOS','Postgraduate Research','Schools','Non-Award','Foreign Affairs/Defence']
loc={fy:{'onshore':v.get('In Australia',0),'offshore':v.get('Outside Australia',0)} for fy,v in d['byFYloc'].items()}

out={
 'generated':'2026-07-20',
 'source':'Department of Home Affairs, BP0015 Student visas granted (subclass 500), via data.gov.au — locked at 31 May 2026',
 'measure':'Primary student visa grants (excludes dependants/secondary applicants)',
 'full_years':d['full_years'], 'partial_label':d['partial'], 'latest_full':'2024-25',
 'sectors':SECTORS,
 'fyTotal':d['fyTotal'],
 'byFYsec':d['byFYsec'],
 'byFYcty':byFYcty,
 'ctySec_latest':ctySec,
 'byFYloc':loc,
 'meta':{
   'note':'Counts are visa GRANTS (offers accepted into a visa), a demand-realised signal — not applications or enrolments. Primary applicants only (the students); dependants excluded. Sector = the education sector of the course the visa was granted for. No individual-provider detail is published, so this is national/sector, not institution-level. Complements CRICOS course supply: this is who is granted visas to come, by source country and sector.',
   'partial':'2025-26 is a partial year (to 31 May 2026) — do not compare its total to full years.',
   'policy':'The 2022-23 peak (~500k) reflects the post-COVID rebound; the fall through 2023-24/2024-25 reflects tightened settings (Ministerial Direction 107 then 111, higher financial/English requirements, and NOSC caps from 2025).'
 }
}
with open('visa_data.js','w') as f:
    f.write('window.VISADEMAND = '); json.dump(out,f,separators=(',',':')); f.write(';\n')
import os
print('visa_data.js', os.path.getsize('visa_data.js'),'bytes')
print('top 2024-25:', sorted(byFYcty['2024-25'].items(),key=lambda x:-x[1])[:5])
print('sector share 2024-25 HE%:', round(d['byFYsec']['2024-25']['Higher Education']/d['fyTotal']['2024-25']*100,1))
