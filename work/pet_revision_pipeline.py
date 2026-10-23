"""Revision orchestration; all mandatory atlas tools remain bundled/unmodified."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, sys, shutil, hashlib
import pet_pipeline as p

p.RUN = p.ROOT / 'work/Pets/rapi-red-hood-v2'
p.OUTPUT_DIR = p.ROOT / 'outputs/rapi-v2'
p.DISPLAY_NAMES = {'jumping':'grounded-chuckle'}
OLD = p.ROOT/'work/Pets/rapi-red-hood'
R=p.RUN

def prepare_reuse():
    for state in ['running-right','running-left']:
        shutil.copyfile(OLD/'decoded'/f'{state}.png',R/'decoded'/f'{state}.png')
    # Both coherent look families and cardinal anchors are already generated and approved.
    for name in ['look-row-9-registered.png','look-row-10.png','look-anchors-approved.png']:
        shutil.copyfile(OLD/'decoded'/name,R/'decoded'/name)
    shutil.copyfile(OLD/'qa/look-row-9-registration.json',R/'qa/look-row-9-registration.json')
    shutil.copyfile(OLD/'qa/direction-semantics.json',R/'qa/direction-semantics.json')

def assemble():
    p.standard()
    p.bundled('assemble_extended_atlas','--base-atlas',R/'final/spritesheet.png','--registered-row-9',R/'decoded/look-row-9-registered.png','--row-9-registration',R/'qa/look-row-9-registration.json','--look-row-10',R/'decoded/look-row-10.png','--output',R/'final/spritesheet-extended-raw.png','--chroma-key','#00FFFF')

def finalprep():
    p.finalprep()

def quality():
    # User explicitly removed the jump. This changes only that semantic threshold.
    p.bundled('validate_pet_quality',R/'final/spritesheet-extended.png','--atlas-validation',R/'final/validation-extended.json','--chroma-report',R/'qa/chroma-despill-extended.json','--frame-review',R/'qa/review.json','--direction-semantics',R/'qa/direction-semantics.json','--continuity',R/'qa/look-continuity.json','--minimum-jump-lift','0','--json-out',R/'qa/pet-quality.json')
    atlas=Image.open(R/'final/spritesheet-extended.png').convert('RGBA')
    bottoms=[]
    for i in range(5):
        alpha=atlas.crop((i*192,4*208,(i+1)*192,5*208)).getchannel('A')
        bottoms.append(alpha.point(lambda a:255 if a>16 else 0).getbbox()[3])
    report={'ok':max(bottoms)-min(bottoms)<=3,'semantics':'grounded-chuckle; jumping explicitly removed by user','foot_baselines':bottoms,'maximum_baseline_difference':max(bottoms)-min(bottoms)}
    (R/'qa/no-jump-check.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
    if not report['ok']:raise SystemExit('Grounded chuckle baseline drift; repair source or registration.')

def previews():
    p.previews()
    out=p.OUTPUT_DIR
    (out/'idle-jump-idle.gif').replace(out/'idle-chuckle-idle.gif')
    (out/'states/jumping.gif').replace(out/'states/grounded-chuckle.gif')
    atlas=Image.open(R/'final/spritesheet-extended.png').convert('RGBA')
    picks=[(0,0,'gentle idle'),(3,2,'teasing wave'),(4,2,'secret chuckle'),(5,3,'gritted teeth'),(6,2,'shy blush'),(8,4,'knowing smirk')]
    sheet=Image.new('RGB',(6*220,250),'#eceef3')
    for j,(row,col,label) in enumerate(picks):
        cell=atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
        sheet.paste(cell,(j*220+14,28),cell)
        ImageDraw.Draw(sheet).text((j*220+10,8),label,fill='#252936')
    sheet.save(out/'expression-stills.png')

if __name__=='__main__':globals()[sys.argv[1]]()
