import json
import time
import requests
from config import API_KEY, SECRET_KEY
import base64 
from PIL import Image 
from io import BytesIO 

class FusionBrainAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        """
        Kullanılabilir ilk pipeline ID'sini döndürür.
        """
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        """
        Görüntü oluşturma isteğini başlatır ve request UUID'sini döndürür.
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {"query": f"{prompt}"}
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        """
        Görüntü oluşturma durumunu kontrol eder ve tamamlandığında Base64 string listesini döndürür.
        """
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files'] 
            attempts -= 1
            time.sleep(delay)
        return None

    def save_image(self, base64_string, file_path):
        """
        Base64 formatındaki veriyi çözer ve belirtilen yola resim olarak kaydeder.
        """
        try:
            decoded_data = base64.b64decode(base64_string)
             
            image = Image.open(BytesIO(decoded_data))
            
            image.save(file_path)
            
            print(f"✅ Görüntü kaydedildi: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Görüntü kaydetme/çözümleme hatası: {e}")
            return False

    def get_image_binary(self, prompt):
        """
        Görüntü oluşturur ve görüntünün ikili verisini (BytesIO) döndürür.
        Bu çıktı, Discord'da doğrudan dosya olarak gönderilebilir.
        """
        try:
            pipeline_id = self.get_pipeline()
            uuid = self.generate(prompt, pipeline_id)
            files = self.check_generation(uuid)

            if not files:
                print("❌ Görüntü oluşturulamadı.")
                return None

            base64_string = files[0] 
            decoded_data = base64.b64decode(base64_string)
            
            return BytesIO(decoded_data) 
        
        except Exception as e:
            print(f"❌ Görüntü oluşturma/veri çekme hatası: {e}")
            return None


def generate_image_from_text(prompt, api_url, api_key, secret_key):
    api = FusionBrainAPI(api_url, api_key, secret_key)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)

    if not files:
        print("❌ Görüntü oluşturulamadı.")
        return None

    image_url = files[0] if isinstance(files, list) else files

    response = requests.get(image_url)  
    if response.status_code == 200: 
        with open("output.png", "wb") as f: 
            f.write(response.content)   
        print("✅ Görüntü kaydedildi: output.png")  
    else:   
        print("❌ Görüntü indirilemedi.")   

        with open('output.txt', 'w', encoding='utf-8') as f:
            for item in files:
               f.write(f"{item}\n")
 

    return image_url    


if __name__ == '__main__':  
    
    api = FusionBrainAPI(
        "https://api-key.fusionbrain.ai/",  
        API_KEY,
        SECRET_KEY
    )
    
    try:
        pipeline_id = api.get_pipeline()
        uuid = api.generate("A futuristic city at sunset with flying cars", pipeline_id)
        base64_data = api.check_generation(uuid)[0] 
        
        if base64_data:
            api.save_image(base64_data, "test_base64_output.png")
    except Exception:
        pass

    image_link = generate_image_from_text(  
        "A futuristic city at sunset with flying cars", 
        "https://api-key.fusionbrain.ai/",  
        API_KEY,
        SECRET_KEY
    )
    print("Görsel bağlantısı:", image_link)

    try:
        binary_data = api.get_image_binary("A single red poppy field in the wind")
        if binary_data:
            print(f"✅ get_image_binary testi başarılı. İkili veri (BytesIO) hazır.")
    except Exception:
        pass