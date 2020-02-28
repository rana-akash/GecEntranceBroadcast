import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

sys.path.append('/usr/local/lib/python2.7/dist-packages')

block_blob_service = BlockBlobService(account_name='csg69dee830b976x4669xabc', account_key='K4cp8mGb+/a4DdfQaq/qAlP6hSbnclcs39C7zwehMIbwodbd3/il162NTmzjLnXWkvIRW3ELOyDKEOs+jMjiEw==')

container_path="/home/pi/GecEntrance/Container"
pdf_path="/home/pi/GecEntrance/Pdfs"
img_path="/home/pi/GecEntrance/Images"
local_files=[]
img_files=[]

for r,d,f in os.walk(container_path):
    for file in f:
        #print(file)
        local_files.append(os.path.join(file))
        
print("List of blobs")
generator = block_blob_service.list_blobs('gec2entrance')

server_files=[]
flag=False

for blob in generator:
    print("Blob Name" + blob.name)
    server_files.append(blob.name)
    full_path = os.path.join(container_path,blob.name)
    if(blob.name not in local_files):
        block_blob_service.get_blob_to_path('gec2entrance',blob.name,full_path)
        print("Downloaded: " + blob.name)
        os.system('libreoffice --headless --convert-to pdf /home/pi/GecEntrance/Container/'+blob.name+' --outdir /home/pi/GecEntrance/Pdfs')
        print("PDF generated "+blob.name)
        os.system('convert -quality 100 -density 300 '+pdf_path+'/'+blob.name[:-4]+'pdf '+img_path+'/'+blob.name[:-4]+'png')
        print("IMG generated "+blob.name)
        print('is changed   '+os.environ["ischanged"])
        #os.environ["ischanged"]="true"
        flag=True
        
    else:
        print("File already present")

for r,d,f in os.walk(img_path):
    for file in f:
        #print(file)
        img_files.append(os.path.join(file))
        

        
for file in local_files:
    if(file not in server_files):
        os.remove(container_path+"/"+file)
        os.remove(pdf_path+"/"+file[:-4]+"pdf")
        for ifile in img_files:
            #print('try remove '+ifile)
            #print('compare '+file[0:25]+ 'with '+ifile[0:25])
            if (ifile[0:25] == file[0:25]):
                os.remove(img_path+ '/'+ifile)
        flag=True
        print("Removed:"+file[:-5])
        
if (flag):
    sys.exit(0)
else:
    sys.exit(1)