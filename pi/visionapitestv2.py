import os, io 
import glob
import time
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'visionApi.json'


client = vision.ImageAnnotatorClient()
client.annotate_image({
  'image': {'source': {'image_uri': 'https://www.google.com/search?q=uri+vs+url&rlz=1C1CHBF_enCA919CA919&sxsrf=ALeKk01bix9U18zGhifN-BUJkdQTQiIhgA:1612647456260&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjup5z2m9buAhVLEVkFHUGhDBkQ_AUoAXoECBwQAw&biw=1920&bih=969#imgrc=Na19ocdh5OhqhM'}},
  'features': [{'type_': vision.Feature.Type.FACE_DETECTION}]
})


def detect_faces(id):
    frames=glob.glob('./*id'+str(id)+'.jpg')
    people_shop_count=0
    checkppe=False
    #start_time = time.time()
    if len(frames)>0:
        path= frames[-1]

        with io.open(path, 'rb') as image_file:
                content = image_file.read()

        image = vision.Image(content=content)

        response = client.annotate_image({
        'image': image,
        'features': [{'type_': vision.Feature.Type.FACE_DETECTION},{'type_': vision.Feature.Type.OBJECT_LOCALIZATION},{'type_': vision.Feature.Type.LABEL_DETECTION , 'max_results':50}]
        })
        faces = response.face_annotations
        pp=["Person"]
        #person = [d for d in response.localized_object_annotations if d["name"] in pp]
        person= list(filter(lambda d: d.name == "Person", response.localized_object_annotations))
        
        for ppecheck in response.label_annotations:
            if ppecheck.description == "Personal protective equipment":
                checkppe=True
                break


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
    return {'count': people_shop_count, 'ppecheck': checkppe , 'path': path}


def main():
    store_count=0
    id_num=0
    while 1:
        images_path_before= glob.glob('./*id'+str(id_num)+'.jpg')
        time.sleep(.101)
        if len(images_path_before)>0:
            images_path_after= glob.glob('./*id'+str(id_num)+'.jpg')
            if len(images_path_before)!=len(images_path_after):
                face_result= detect_faces(id_num)
                # face result could be logged
                id_num+=1
                store_count+=face_result["count"]

        #break


if __name__ == "__main__":
    main()