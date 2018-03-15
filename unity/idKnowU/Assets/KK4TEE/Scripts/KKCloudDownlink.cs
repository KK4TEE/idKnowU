using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class KKCloudDownlink : MonoBehaviour
{

    public string cloudserver = "https://127.0.0.1:8088";
    public string MasterJsonURL = "/jsonImages";
    public float refreshrate = 2.0f;

    public GameObject HUDHolder;
    public TextMesh TextName;
    public TextMesh TextSocial;
    public TextMesh TextRole;
    public TextMesh TextFunFact;
    public TextMesh TextAccuracy;
    

    public JObject CloudJObj;
    //public JObject LocalDeviceJObj = new JObject();
    //public JObject arSettings = new JObject();
    bool jsonAvailable = false;


    IEnumerator DownloadCloudJSON()
    {
        string url = cloudserver + MasterJsonURL;
        WWW www = new WWW(url);
        yield return www;

        CloudJObj = JObject.Parse(www.text);
        if (CloudJObj.HasValues)
        {
            jsonAvailable = true;
            print(CloudJObj["name"]);
            print(CloudJObj["socialMedia"]);
            print(CloudJObj["role"]);
            print(CloudJObj["funFact"]);
            print(CloudJObj["accuracy"]);

            TextName.text = CloudJObj["name"].Value<string>();
            TextSocial.text = CloudJObj["socialMedia"].Value<string>();
            TextRole.text = CloudJObj["role"].Value<string>();
            TextFunFact.text = CloudJObj["funFact"].Value<string>();
            TextAccuracy.text = CloudJObj["accuracy"].Value<string>();
            //SetTargetVisible(HUDHolder, true);
            
        }
        else
        {
            jsonAvailable = false;
            //SetTargetVisible(HUDHolder, false);
        }
        

    }
    


    void UpdateHelper()
    {
        StartCoroutine(DownloadCloudJSON());
    }


    void SetTargetVisible(GameObject Target, bool viz)
    {
        Component[] a = Target.GetComponentsInChildren(typeof(Renderer));
        foreach (Component b in a)
        {
            Renderer c = (Renderer)b;
            if (viz == true)
            {
                c.enabled = true;
            }
            else
            {
                c.enabled = false;
            }
        }
    }
    // Use this for initialization
    void Start()
    {
        InvokeRepeating("UpdateHelper", 2.0f, refreshrate); //Start after 2 seconds, repeat every refreshrate
        
        
    }

    // Update is called once per frame
    void Update()
    {
        //pass
    }
}
