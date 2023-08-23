import os

def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def actualPath(fp):
    if debugMode():
        print("actualPath",fp)

    fdir = os.path.dirname(fp)
    fbase = os.path.basename(fp)
        
    if os.path.exists(fp):
        # the file exists, check for case match
        # by reading the actual filenames from the directory
        dlist = os.listdir(fdir)
        for f in dlist:
            # all OK, we have a match
            if f == fbase:
                return fp
            # check for case mismatch
            if f.upper() == fbase.upper():
                # return the correct case
                return fdir+"/"+f
        
    else:
        # return a missing file
        return missing_image_path
#
# Function to empty a directory
#
def EmptyDir(d):
    if debugMode():
        print("EmptyDir",d)

    if d==None:
        return
    
    if os.path.isdir(d):
      files=os.walk(d)
      
      # delete all the files
      for item in files:
          for sdir in item[1]:
              EmptyDir(item[0]+os.sep+sdir)
          for f in item[2]:
              ff = item[0]+os.sep+f
              os.remove(ff)
              if debugMode():
                print("  removed",ff)
    else:
        os.mkdir(d)
        print("created",d)
    # delete any subdirectories
    dirs = os.walk(d)
    for dd in dirs:
        for ddir in dd[1]:
            EmptyDir(dd[0]+os.sep+ddir)
            os.rmdir(dd[0]+os.sep+ddir)

    if debugMode():
        print("all files deleted from",d)
        
#
# Function to make a display format date for titles.
#
def titleDate(crd):
    if debugMode():
        print("titleDate",crd)

    pmonth = ["January","February","March","April","May"]
    pmonth2 = ["June","July","August","September","October","November","December"]
    pmonth = pmonth+pmonth2

    yr = crd[:4]
    mon = int(crd[4:6])
    day = crd[6:8]
    
    return pmonth[mon-1]+" "+day+", "+yr
