using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridScript : MonoBehaviour
{
    public int width;
    public int height;
    public float separation = 1.1f;

    [Range(0, 1)]
    public float obstactleFreq;
    [Range(0, 1)]
    public float goalFreq;

    List<GameObject> entities;
    GameObject plane;
    GameObject[,] grid;

    // Start is called before the first frame update
    void Start()
    {
        int obstacleQuantity = (int) (100 * obstactleFreq);
        int goalQuantity = (int)(100 * goalFreq);

        entities = new List<GameObject>();
        grid = new GameObject[width, height];
        plane = GameObject.CreatePrimitive(PrimitiveType.Plane);

        plane.transform.parent = transform;
        plane.transform.position = new Vector3(width / 2, 0, height / 2);
        plane.transform.localScale = new Vector3(width * .1f, 1, height * .1f);

        // Instantiate prefabs
        for (int i = 0; i < obstacleQuantity; i++)
        {
            GameObject obj = InstantiatePrefab("Prefabs/Obstacle", "Obstacle " + i, "Entities");
            entities.Add(obj);
        }
        for (int i = 0; i < goalQuantity; i++)
        {
            GameObject obj = InstantiatePrefab("Prefabs/Goal", "Goal " + i, "Entities");
            entities.Add(obj);
        }

        // Shuffle
        for (int i = 0; i < entities.Count; i++)
        {
            GameObject temp = entities[i];
            int randomIndex = Random.Range(i, entities.Count);
            entities[i] = entities[randomIndex];
            entities[randomIndex] = temp;
        }

        // Populate the grid
        int taken = 0;
        while (taken < entities.Count)
        {
            int x = UnityEngine.Random.Range(0, width);
            int y = UnityEngine.Random.Range(0, height);

            if (grid[x, y] == null)
            {
                grid[x, y] = entities[taken];
                grid[x, y].transform.localPosition = new Vector3(x, 0, y);
                taken++;
            }
        }

        //grid[width - 1, height - 1] = entities[0];
        //grid[width - 1, height - 1].transform.position = new Vector3(width - 1, 0, height - 1);

        // Apply separation
        //for (int x = 0; x < width; x++)
        //{
        //    for (int y = 0; y < height; y++)
        //    {
        //        if (grid[x, y] != null)
        //        {
        //        }

        //    }
        //}
    }

    // Update is called once per frame
    void Update()
    {

    }

    GameObject InstantiatePrefab(string location, string objName, string parentLocation)
    {
        GameObject clone = Instantiate(Resources.Load<GameObject>(location));
        clone.name = objName;
        clone.transform.parent = GameObject.Find(parentLocation).transform;
        clone.transform.localPosition = new Vector3(0, 0, 0);
        return clone;
    }
}
