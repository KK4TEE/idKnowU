using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class KKCloudUplink : MonoBehaviour {

    public string cloudserver = "http://127.0.0.1.com:8088";
    public string functionURL = "/upload";
    public float refreshrate = 2.0f;
    public bool UploadEnabled = true;
    public bool isUploading = false;

    //public JObject CloudJObj;
    

    public JObject LocalDeviceJObj = new JObject();
    public JObject arSettings = new JObject();
    public GameObject TrackedGameObject;
    bool jsonAvailable = false;
    KKTools KKT = new KKTools();

    public JObject UpdateLocalDeviceData(JObject j)
    {
        
        j["unixtime"] = KKT.UnixTime().ToString();
        //j["GPS"]["FIX"] = "false";

        return j;
    }

    public IEnumerator UploadCloudJSON()
    {
        isUploading = true;
        JObject jObjToUpload = LocalDeviceJObj;
        jObjToUpload = UpdateLocalDeviceData(jObjToUpload);
        //jObjToUpload.Add("device", jObj["sensors"]);
        jObjToUpload["settings"] = arSettings;

        string url = cloudserver + functionURL;

        var request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(jObjToUpload));
        request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");
        request.chunkedTransfer = false;

        yield return request.SendWebRequest();
       
        //foreach (string key in request.GetResponseHeaders().Keys)
        //{ print(key);  }


        //print(request.GetResponseHeader("data"));
        //returnedstring = www.ToString();
        //print(returnedstring);
        isUploading = false;

    }


    public void UpdateHelper()
    {
        if (UploadEnabled && !isUploading)
        {
            isUploading = true;
            StartCoroutine(UploadCloudJSON());
        }
        
    }

    public void InitializeJSONSensors()
    {
        
        arSettings.Add("deviceUniqueIdentifier", SystemInfo.deviceUniqueIdentifier);
        arSettings.Add("deviceName", SystemInfo.deviceName);
        arSettings.Add("version", Application.version);
        arSettings.Add("genuine", Application.genuine.ToString());
        arSettings.Add("internetReachability", Application.internetReachability.ToString());
        arSettings.Add("platform", Application.platform.ToString());
        arSettings.Add("unix_startime", KKT.UnixTime().ToString());
        print("KKCloudUplink has started");
        
    }
    // Use this for initialization
    void Start () {
        InvokeRepeating("UpdateHelper", 2.0f, refreshrate); //Start after 2 seconds, repeat every refreshrate
        InitializeJSONSensors();
    }
	
	// Update is called once per frame
	void Update () {
		//pass
	}
}
