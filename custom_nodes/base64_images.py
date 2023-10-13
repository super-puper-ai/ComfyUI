import base64
from PIL import Image
import numpy as np
from io import BytesIO
import requests

class ImageToBase64:

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {"images": ("IMAGE", ),},
                }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "image_to_base64"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def image_to_base64(self, images):
        print("======image_to_base64=======")
        results = list()
        count=0
        for image in images:
            print("images: " + str(count))
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            img.save(buffer, format="PNG")                  #Enregistre l'image dans le buffer
            myimage = buffer.getvalue()  
            encoded_string = "data:image/jpeg;base64," + base64.b64encode(myimage).decode('ascii')
            
            results.append({
                "index": count,
                "base64": encoded_string
            })
            count=count+1
        return (results,)

class SendBase64Images:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": 
                    {
                        "images": ("CONDITIONING", ),
                        "callBackApi": ("STRING", {"multiline": False})
                    },
                }
    
    RETURN_TYPES = ()
    FUNCTION = "request"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def request(self, images, callBackApi):
        print("====================")
        x=requests.post(callBackApi, json=images)
        return ()


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageToBase64": ImageToBase64,
    "SendBase64Images": SendBase64Images
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToBase64": "Image To Base64",
    "SendBase64Images": "Send Base64 Images"
}