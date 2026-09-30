from watermarker.marker import  add_mark
import os
import shutil


def mark(file, outdir, mark = "火苗999℃"):
    add_mark(file = file, out = outdir, mark = mark
            #, color = "#000000"
            , opacity=0.15, angle=30, space=200, size=20)
    return 


def mark_dir2(root, out):
    if not os.path.exists(out):
        # os.path.isdir(out):
        os.mkdir(out)
    files = os.listdir(root)
    for fname in files:
        fpath = root + "\\" + fname
        if os.path.isfile(fpath):   # not a dir
            file_name, file_extension = os.path.splitext(fname)
            if ".gif" == file_extension:
                shutil.copy(fpath, out + "\\" + fname)
            else:
                mark(fpath, out)
        elif os.path.isdir(fpath):  # is a dir
            subdir = root + "\\" + fname
            subout =  out + "\\" + fname
            if "linux-network-traffic" == fname:
                shutil.rmtree(subout)
                shutil.copytree(subdir, subout, copy_function = shutil.copy)
                continue
            elif "cover" == fname:
                shutil.rmtree(subout)
                shutil.copytree(subdir, subout, copy_function = shutil.copy)
            elif "nomark" == fname:
                shutil.rmtree(subout)
                shutil.copytree(subdir, subout, copy_function = shutil.copy)
            else:
                mark_dir2(subdir, subout)
        else :
            print("no defined {}!".format(fpath))
    return 

if __name__ == '__main__' :
    src = 'H:\\myblog\\blog\\source\\picture\\src'
    out = 'H:\\myblog\\blog\\source\\picture\\mark'
    mark_dir2(src, out)
