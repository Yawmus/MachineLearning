using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class EntityScript : MonoBehaviour
{
    GameObject score;

    private void OnTriggerEnter(Collider other)
    {
        WasHit();
    }
    private void OnTriggerStay(Collider other)
    {
        WasHit();
    }

    private void WasHit()
    {
        if(GetComponent<Renderer>().enabled == false)
        {
            return;
        }

        string temp = score.GetComponent<Text>().text;
        int newScore = Convert.ToInt32(temp.Split(' ')[1]);

        newScore += name.Contains("Obstacle") ? -1 : 1;
        score.GetComponent<Text>().text = "Score: " + newScore;
        GetComponent<Renderer>().enabled = false;
    }

    // Start is called before the first frame update
    void Start()
    {
        score = GameObject.Find("Score");
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
