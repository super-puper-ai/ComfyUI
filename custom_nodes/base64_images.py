import base64
from PIL import Image
import numpy as np
from io import BytesIO
import requests
import urllib.parse


class ImageToBuffer:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "image_to_buffer"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def image_to_buffer(self, images):
        print("======image_to_buffer=======")
        results = list()
        count = 0
        for image in images:
            print("images: " + str(count))
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            results.append(buffer)
        return (results,)


class SendBufferedImages:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                {
                    "images": ("CONDITIONING", ),
                    "callBackApi": ("STRING", {"multiline": False})
                },
                "hidden": {"prompt_id": "PROMPT_ID"},
                }

    RETURN_TYPES = ()
    FUNCTION = "send"
    OUTPUT_NODE = True
    CATEGORY = "image"

    def send(self, images, callBackApi, prompt_id):
        cbHost = urllib.parse.unquote(callBackApi)
        payload = {
            "promptId": prompt_id,
        }
        files = []
        for i, image in enumerate(images):
            image.seek(0)
            files.append((str(i), ('my.png', image, 'image/png')))
        print(payload)
        x = requests.post(cbHost, data=payload, files=files, verify=False)
        print(x)
        # x = requests.post('https://192.168.0.100:443/generation1saveresult', data=payload, files=files, verify=False)
        print(x)
        return ()


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageToBuffer": ImageToBuffer,
    "SendBufferedImages": SendBufferedImages
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToBuffer": "Image to buffer",
    "SendBufferedImages": "Send buffered images"
}
