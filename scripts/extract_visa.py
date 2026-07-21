import zipfile, xml.etree.ElementTree as ET, json, time
NS='{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
z=zipfile.ZipFile('visa_granted.xlsx')

# shared items per field (index -> value)
root=ET.fromstring(z.read('xl/pivotCache/pivotCacheDefinition1.xml'))
fields=root.findall(f'.//{NS}cacheField')
shared=[]
for cf in fields:
    si=cf.find(f'{NS}sharedItems'); vals=[]
    if si is not None:
        for c in si:
            tag=c.tag.split('}')[1]
            vals.append(c.attrib.get('v') if tag=='s' else None)
    shared.append(vals)
names=[cf.attrib['name'] for cf in fields]
FY,LOC,SEC,APP,CTY,TOT = names.index('Financial Year of Visa Grant'),names.index('Client Location'),names.index('Sector'),names.index('Applicant Type'),names.index('Citizenship Country'),names.index('Total')

FULL=['2005-06','2006-07','2007-08','2008-09','2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21','2021-22','2022-23','2023-24','2024-25']
PARTIAL='2025-26 to 31 May 2026'
KEEP=set(FULL+[PARTIAL])
SEC_SHORT={'Higher Education Sector':'Higher Education','Vocational Education and Training Sector':'VET','Independent ELICOS Sector':'ELICOS','Schools Sector':'Schools','Non-Award Sector':'Non-Award','Postgraduate Research Sector':'Postgraduate Research','Foreign Affairs or Defence Sector':'Foreign Affairs/Defence'}

byFYsec={}; byFYcty={}; ctySec_latest={}; byFYloc={}; fyTotal={}
t0=time.time(); n=0
with z.open('xl/pivotCache/pivotCacheRecords1.xml') as f:
    for ev,el in ET.iterparse(f, events=('end',)):
        if el.tag!=f'{NS}r': continue
        kids=list(el)
        def val(i):
            c=kids[i]; tag=c.tag.split('}')[1]
            if tag=='x': return shared[i][int(c.attrib['v'])]
            if tag=='s': return c.attrib.get('v')
            if tag=='n': return c.attrib.get('v')
            return None
        fy=val(FY)
        if fy in KEEP:
            app=val(APP)
            if app=='Primary':                      # students, not dependents
                sec=SEC_SHORT.get(val(SEC),val(SEC)); cty=val(CTY); loc=val(LOC)
                try: tot=int(float(kids[TOT].attrib.get('v',0)))
                except: tot=0
                byFYsec.setdefault(fy,{}); byFYsec[fy][sec]=byFYsec[fy].get(sec,0)+tot
                byFYcty.setdefault(fy,{}); byFYcty[fy][cty]=byFYcty[fy].get(cty,0)+tot
                byFYloc.setdefault(fy,{}); byFYloc[fy][loc]=byFYloc[fy].get(loc,0)+tot
                fyTotal[fy]=fyTotal.get(fy,0)+tot
                if fy=='2024-25':
                    ctySec_latest.setdefault(cty,{}); ctySec_latest[cty][sec]=ctySec_latest[cty].get(sec,0)+tot
        el.clear()
        n+=1
        if n%400000==0: print(f'{n} records, {time.time()-t0:.0f}s')

json.dump({'byFYsec':byFYsec,'byFYcty':byFYcty,'byFYloc':byFYloc,'ctySec_latest':ctySec_latest,'fyTotal':fyTotal,
           'full_years':FULL,'partial':PARTIAL}, open('visa_agg.json','w'))
print('done', n, 'records in', round(time.time()-t0), 's')
print('FY totals (Primary):', {k:fyTotal[k] for k in FULL[-5:]+[PARTIAL]})
print('sectors 2024-25:', byFYsec.get('2024-25'))
