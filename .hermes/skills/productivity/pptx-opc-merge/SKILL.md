---
name: pptx-opc-merge
description: Merge multiple PPTX files at the OPC level using zipfile + lxml, bypassing python-pptx's broken clone_slide
tags:
  - python-pptx
  - pptx
  - opc
  - merge
  - zipfile
---

# PPTX OPC-Level Merge Skill

## When to Use
Merging multiple `.pptx` files into one, especially when python-pptx's `clone_slide` or `add_slide` produces files with empty/corrupt content despite correct slide counts.

## The Problem
`python-pptx` cannot reliably clone slides between presentations with different layouts. The `clone_slide` approach using `deepcopy` + `prs.slides._sldIdLst.append()` produces a file that passes `len(prs.slides)` but renders empty when opened — because the OPC relationship IDs (rIds) connecting slides to their layouts are not remapped.

## The Solution: OPC-Level Merge

### Python interpreter
```bash
/tmp/ocr_env/bin/python   # has python-pptx installed
```

### Approach
Directly manipulate the `.pptx` OPC (Open Packaging Conventions) structure using `zipfile` + `lxml`:

1. Extract each slide's XML bytes from every source `.pptx`
2. Remap rIds in slide XML and their `.rels` files
3. Rebuild `ppt/presentation.xml` with correct `sldIdLst`
4. Rebuild `ppt/_rels/presentation.xml.rels` with correct slide relationships
5. Rebuild `[Content_Types].xml`
6. Write a new `.zip` as the merged `.pptx`

### Key Code Patterns

**Slide rId remapping:**
```python
from lxml import etree
from copy import deepcopy

# Parse slide rels
rels_root = etree.fromstring(sld_rels_xml)
new_rels_root = etree.fromstring(
    b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"></Relationships>'
)

rId_map = {}
for rel in rels_root.findall('Relationship'):
    old_rId = rel.get('Id')
    new_rId = f"rId{rId_counter}"
    rId_map[old_rId] = new_rId
    rel.set('Id', new_rId)
    new_rels_root.append(deepcopy(rel))
    rId_counter += 1

# Remap rIds in slide XML
for elem in sld_root.iter():
    for attr in ('id', 'r:id'):
        val = elem.get(attr)
        if val and val in rId_map:
            elem.set(attr, rId_map[val])
```

**presentation.xml sldIdLst (critical):**
```python
# sldId.id must be unique integer, r:id must match presentation.xml.rels
sldId_elem.set('id', str(256 + i))
sldId_elem.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id', slide_rid)
```

**presentation.xml.rels relationship:**
```xml
<Relationship Id="rId{num}" 
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" 
  Target="slides/slide{i}.xml"/>
```

## Critical Bug: rId Counter Must Advance Per Slide

If `rid_counter` is incremented once per source PPTX (not once per slide), every slide in the merged file will get the **same rId** → all slides render identically (the last slide's content). 

**Symptom:** `len(prs.slides)` is correct (e.g. 42) but opening the file shows the same content on every non-first slide.

**Verification:** Read `ppt/presentation.xml`, check that every `p:sldId` element has a **different** `r:id` value. If they all say `rId199`, the counter bug is present.

**Fix:** Increment `rid_counter` inside the per-slide loop, not the per-source-PPTX loop:
```python
for src_path, src_sld, new_sld in all_slides:   # per-slide loop
    rid_counter += 1     # MUST be here, not outside
    rid = f"rId{rid_counter - 1}"
    slide_refs.append((str(sld_id), rid))
```

## Symptom Diagnosis

| Symptom | Cause | Fix |
|---------|-------|-----|
| All slides after slide 1 show same content | `rid_counter` not advancing per-slide (all got same rId) | Increment rid_counter **inside** per-slide loop |
| File "format invalid" when opened in WeChat/Office | Missing required OPC relationships or Content_Types | Verify all required parts exist; use working source as base |
| `len(prs.slides)` correct but content wrong | python-pptx internal state broken | Always verify with `zipfile + etree` text extraction |

## Key Lesson
Never trust `len(prs.slides)` after a merge — verify actual XML content by extracting text from the saved `.pptx` using `zipfile + etree.findall('.//{...drawingml/2006/main}t')`. A visually correct slide count means nothing if the rIds aren't wired up.

**Verification checklist:**
```python
import zipfile, re
from lxml import etree

z = zipfile.ZipFile('output.pptx')
pres = z.read('ppt/presentation.xml')
root = etree.fromstring(pres)
sldIdLst = root.find('.//{...presentationml/2006/main}sldIdLst')
rids = [s.get('{...officeDocument/2006/relationships}id') for s in sldIdLst]
print(f'Unique rIds: {len(set(rids))} / {len(rids)}')  # must be equal
```

## Source File
- `/home/agentuser/merge_v3.py` — working OPC merger with per-slide rId counter (corrected)
- `/home/agentuser/merge_opc.py` — first working version
- `/home/agentuser/merge_all_works.py` — BROKEN (rId counter bug)
