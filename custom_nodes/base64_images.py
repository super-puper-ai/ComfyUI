import torch
import base64
from PIL import Image, ImageOps
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
            print("Image.fromarray")
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            print("Image.save")
            img.save(buffer, format="PNG", optimize=False)
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


class Base64ToImage:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base64Str": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE","MASK")
    FUNCTION = "base64_to_image"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def base64_to_image(self, base64Str):
        _bytes = base64.decodebytes(bytes(base64Str, 'utf-8'))
        i = Image.open(BytesIO(_bytes))
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (image, mask.unsqueeze(0))


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ImageToBuffer": ImageToBuffer,
    "SendBufferedImages": SendBufferedImages,
    "Base64ToImage": Base64ToImage,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageToBuffer": "Image to buffer",
    "SendBufferedImages": "Send buffered images",
    "Base64ToImage": "Base64 To Image",
}
