import os, io, shutil
import glob
import time
from pygame import mixer
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'visionApi.json'


client = vision.ImageAnnotatorClient()
client.annotate_image({
  'image': {'source': {'image_uri': 'https://www.google.com/search?q=uri+vs+url&rlz=1C1CHBF_enCA919CA919&sxsrf=ALeKk01bix9U18zGhifN-BUJkdQTQiIhgA:1612647456260&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjup5z2m9buAhVLEVkFHUGhDBkQ_AUoAXoECBwQAw&biw=1920&bih=969#imgrc=Na19ocdh5OhqhM'}},
  'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
})

mixer.init()
mixer.music.load('wear_a_mask.wav')


def detect_faces(id):
    path=""
    frames=glob.glob('./*'+str(id)+'.jpg')
    people_shop_count=0
    checkppe=False
    print(frames)
    #start_time = time.time()
    if len(frames)>0:
        if "leaving" in frames[0]:
           path= frames[0] 
        else:
            path = frames[-1]

        with io.open(path, 'rb') as image_file:
                content = image_file.read()

        image = vision.Image(content=content)

        response = client.annotate_image({
        'image': image,
        'features': [{'type_': vision.Feature.Type.FACE_DETECTION},{'type_': vision.Feature.Type.OBJECT_LOCALIZATION},{'type_': vision.Feature.Type.LABEL_DETECTION , 'max_results':50}]
        })
        faces = response.face_annotations
        #person = [d for d in response.localized_object_annotations if d["name"] in pp]
        person= list(filter(lambda d: d.name == "Person", response.localized_object_annotations))
        
        for ppecheck in response.label_annotations:
            if ppecheck.description == "Personal protective equipment":
                #print(ppecheck)
                checkppe=True
                break
            #print(ppecheck)
        

        num_faces=len(faces)
        num_person=len(person)
        if num_faces<num_person:
            people_shop_count-= num_person-num_faces
        else :
            people_shop_count += num_faces
        
        #print(person)
        
       # print("--- %s seconds ---" % (time.time() - start_time))
        
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        
        #move and delete files
        destination= "used_pic"+path[1:]
        print(destination)
        shutil.move(path, destination )
        frames.remove(path)
        for pics in frames:
            print("".join(os.path.abspath(os.getcwd()),pics[2:]))
            os.remove(os.path.join(os.path.abspath(os.getcwd()),pics[2:]))
    return {'count': people_shop_count, 'ppecheck': checkppe , 'path': path, 'time': time.time()}


def main():
    store_count=0
    id_num=2
    while 1:
        images_path_before= glob.glob('./*id'+str(id_num)+'.jpg')
        time.sleep(.101)
        if len(images_path_before)>0:
            images_path_after= glob.glob('./*id'+str(id_num)+'.jpg')
            if len(images_path_before)==len(images_path_after):
                face_result= detect_faces(id_num)
                if (face_result["count"]>=0) and not face_result["ppecheck"]:
                    mixer.music.play()
#______________________________________________________________________________________________
                # face_result could be logged
                # {
                #   "count": int number of people, negative for people leaving, positve for people entering
                #   "ppechack": bool, True== persone has a mask, False== could not detect mask
                #   "path": the image path that was used the send to google
                #   "time": timestamp of the return function
                # }
                #
#______________________________________________________________________________________________
                id_num+=1
                store_count+=face_result["count"]
                ppecheck=face_result["ppecheck"]
                print(f"store count: {store_count}\t was there a ppe : {ppecheck} \t id number: {id_num}")

        #break


if __name__ == "__main__":
    main()