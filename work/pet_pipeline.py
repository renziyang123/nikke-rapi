"""Convenience runner for the unmodified bundled pet tools and final previews."""
from pathlib import Path
import json, subprocess, sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / 'work/Pets/rapi-red-hood'
OUTPUT_DIR = ROOT / 'outputs/rapi'
DISPLAY_NAMES = {}
SKILL = Path('C:/Users/z/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/scripts')
STATES = [('idle',6),('running-right',8),('running-left',8),('waving',4),('jumping',5),('failed',8),('waiting',6),('running',6),('review',6)]

def bundled(name,*args):
    subprocess.run([sys.executable,str(SKILL / (name+'.py')),*map(str,args)],check=True)

def standard():
    bundled('extract_strip_frames','--decoded-dir',RUN/'decoded','--output-dir',RUN/'frames','--method','auto','--chroma-key','#00FFFF')
    bundled('inspect_frames','--frames-root',RUN/'frames','--json-out',RUN/'qa/review.json','--require-components')
    bundled('compose_atlas','--frames-root',RUN/'frames','--output',RUN/'final/spritesheet.png')
    bundled('make_contact_sheet',RUN/'final/spritesheet.png','--output',RUN/'qa/contact-sheet.png','--scale','0.75')
    bundled('render_animation_previews','--frames-root',RUN/'frames','--output-dir',RUN/'qa/standard-previews')

def finalprep():
    bundled('despill_chroma_edges',RUN/'final/spritesheet-extended-raw.png','--output',RUN/'final/spritesheet-extended.png','--webp-output',RUN/'final/spritesheet.webp','--json-out',RUN/'qa/chroma-despill-extended.json','--chroma-key','#00FFFF')
    bundled('validate_atlas',RUN/'final/spritesheet-extended.png','--require-v2','--chroma-key','#00FFFF','--json-out',RUN/'final/validation-extended.json')
    bundled('make_contact_sheet',RUN/'final/spritesheet-extended.png','--output',RUN/'qa/final-contact-sheet.png','--scale','0.75')
    bundled('make_direction_qa_sheet',RUN/'final/spritesheet-extended.png','--output',RUN/'qa/direction-sheet.png')
    bundled('measure_direction_continuity',RUN/'final/spritesheet-extended.png','--json-out',RUN/'qa/look-continuity.json')
    bundled('make_direction_blind_qa_sheet',RUN/'final/spritesheet-extended.png','--output',RUN/'qa/direction-blind.png','--answer-key',RUN/'qa/direction-blind-key.json')

def previews():
    """Extract exact encoded cells, then render motion without altering artwork."""
    atlas=Image.open(RUN/'final/spritesheet-extended.png').convert('RGBA')
    out=OUTPUT_DIR
    out.mkdir(parents=True,exist_ok=True)
    frames_root=RUN/'final/encoded-frames'
    for row,(state,count) in enumerate(STATES):
        d=frames_root/state; d.mkdir(parents=True,exist_ok=True)
        for col in range(count):
            atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208)).save(d/f'{col:02}.png')
    bundled('render_animation_previews','--frames-root',frames_root,'--output-dir',out/'states')
    sys.path.insert(0,str(ROOT/'work/python-deps'))
    import imageio_ffmpeg
    allframes=[]; alldurations=[]
    for row,(state,count) in enumerate(STATES):
        for col in range(count):
            cell=atlas.crop((col*192,row*208,(col+1)*192,(row+1)*208))
            panel=Image.new('RGB',(384,256),'#eceef3')
            panel.paste(cell,(96,36),cell)
            ImageDraw.Draw(panel).text((12,12),f'{DISPLAY_NAMES.get(state,state)} / frame {col+1}',fill='#252936')
            allframes.append(panel); alldurations.append(140 if col<count-1 else 420)
    allframes[0].save(out/'all-states.gif',save_all=True,append_images=allframes[1:],duration=alldurations,loop=0,disposal=2)
    encoder=imageio_ffmpeg.write_frames(str(out/'all-states.mp4'),(384,256),fps=25,codec='libx264',pix_fmt_in='rgb24',pix_fmt_out='yuv420p',macro_block_size=1)
    encoder.send(None)
    for f,ms in zip(allframes,alldurations):
        for _ in range(round(ms/40)):encoder.send(f.tobytes())
    encoder.close()
    cells=[Image.open(frames_root/'idle'/f'{i:02}.png') for i in range(6)]
    cells += [Image.open(frames_root/'jumping'/f'{i:02}.png') for i in range(5)]
    cells += [Image.open(frames_root/'idle'/f'{i:02}.png') for i in range(6)]
    cells[0].save(out/'idle-jump-idle.gif',save_all=True,append_images=cells[1:],duration=160,loop=0,disposal=2)
    looks=[atlas.crop((i%8*192,(9+i//8)*208,(i%8+1)*192,(10+i//8)*208)) for i in range(16)]
    looks[0].save(out/'look-loop.gif',save_all=True,append_images=looks[1:],duration=180,loop=0,disposal=2)
    still=Image.new('RGB',(384*4,256),'#eceef3')
    for i,idx in enumerate([0,22,27,45]):still.paste(allframes[idx],(384*i,0))
    still.save(out/'motion-stills.png')
    print(json.dumps({'ok':True,'output':str(out)}))

if __name__=='__main__':
    globals()[sys.argv[1]]()
