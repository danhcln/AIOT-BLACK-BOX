import os, shutil

svg_dir = 'AIOT_BLACKBOX_PRESENTATION_A4_REV5.svg'
if os.path.isdir(svg_dir):
    inner = os.path.join(svg_dir, 'AIOT_BLACKBOX_PRESENTATION.svg')
    if os.path.exists(inner):
        shutil.copy(inner, 'temp_rev5.svg')
        shutil.rmtree(svg_dir)
        os.rename('temp_rev5.svg', svg_dir)
        print("Successfully made AIOT_BLACKBOX_PRESENTATION_A4_REV5.svg a file!")
    else:
        print("Inner file not found in directory")
elif os.path.isfile(svg_dir):
    print("Already a file!")

st = os.stat(svg_dir)
print(f"File: {svg_dir}, Size: {st.st_size} bytes")
