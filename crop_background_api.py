import requests
import sys
import os
import json
url = "https://api.removal.ai/3.0/remove"

if len(sys.argv) >= 3:
	img_path=sys.argv[1]
	img_name=sys.argv[2]
	output_dir=sys.argv[3]
	payload={'image_url': img_path + img_name }
	files=[
	  ('image_file',(img_name,open(img_path + img_name,'rb'),'image/jpeg'))
	]
	headers = {
	  'Rm-Token': '6319e05bd72005.17370944'
	}

	response = requests.request("POST", url, headers=headers, data=payload, files=files)
	text_response = '{"status":200,"preview_demo":"https://file.removal.ai/preview/577d1825-b02b-4f82-9c5d-d7b150bd592c_7.png","url":"https://file.removal.ai/original/577d1825-b02b-4f82-9c5d-d7b150bd592c_7_0B1ZNE.png","high_resolution":"https://file.removal.ai/original/577d1825-b02b-4f82-9c5d-d7b150bd592c_7_0B1ZNE.png","low_resolution":"https://file.removal.ai/low_resolution/577d1825-b02b-4f82-9c5d-d7b150bd592c_7.png","original_width":0,"original_height":0,"preview_width":0,"preview_height":0}'
	data = json.loads(response.text)
	#data = json.loads(text_response)
	print(data)
	cropped_img_url = data["url"]
	response = requests.get(cropped_img_url)
	open(os.path.join(output_dir, img_name.split('.')[0] + '.png'), "wb").write(response.content)
else:
	print(sys.argv)
	
