using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
//using System.IO;

//Based on tutorial example found at https://livierickson.com/blog/5-minute-script-save-webcam-stream-to-image-in-unity-5/
public class KKCameraCapture : KKCloudUplink {
    WebCamTexture _webcamtex;
    public int jpgQuality = 20;
    // Use this for initialization


    public IEnumerator CaptureTextureAsPNG()
    {
        yield return new WaitForEndOfFrame();
        Texture2D _TextureFromCamera = new Texture2D(GetComponent<Renderer>().material.mainTexture.width,
        GetComponent<Renderer>().material.mainTexture.height);
        _TextureFromCamera.SetPixels((GetComponent<Renderer>().material.mainTexture as WebCamTexture).GetPixels());
        _TextureFromCamera.Apply();
        byte[] bytes = _TextureFromCamera.EncodeToJPG(jpgQuality);
        //string filePath = "SavedScreen1.jpg"; // option to save to a local file
        print("CAPTURE_TEXTURE_JPG");
        LocalDeviceJObj["image"]["0"]["base64"] = System.Convert.ToBase64String(bytes);
        StartCoroutine(UploadCloudJSON());

    }


    public void UpdateHelper()
    {
        if (UploadEnabled && !isUploading)
        {
            isUploading = true;
            StartCoroutine(CaptureTextureAsPNG());
        }

    }
    void Start () {
        InitializeJSONSensors();
        InvokeRepeating("UpdateHelper", 2.25f, refreshrate); //Start after 2 seconds, repeat every refreshrate

        LocalDeviceJObj["image"] = new JObject();
        LocalDeviceJObj["image"]["0"] = new JObject();

        _webcamtex = new WebCamTexture();
        Renderer _renderer = GetComponent<Renderer>();
        _renderer.material.mainTexture = _webcamtex;
        _webcamtex.Play();
    }
	
	// Update is called once per frame
	void Update () {
        
    }
}
