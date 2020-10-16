# Set Up Azure Maps

In this step you will set up Azure Maps.

## Steps

1. Go to [Azure portal]('https://portal.azure.com') and login to your subscription. 
2. Create a resource for Azure Maps  ![Azure Maps](../images/azure-maps-create-1.png)
3. Select Azure Maps![Azure Maps](../images/azure-maps-create-2.png)
4. Note down the Primary Key and in [application.js](../server/code/static/js/application.js) and replace <Azure_Map_Subscription_Key> with the primary key
![Azure Maps](../images/azure-maps-create-3.png)
    ```js
    //Initialize a map instance.
    map = new atlas.Map('myMap', {
       ...
        authOptions: {
            authType: 'subscriptionKey',
            subscriptionKey: '<Azure_Map_Subscription_Key>'
        }
    });
    ```
> If you want to learn more about Azure Maps and samples, see [Azure Maps Samples](https://azuremapscodesamples.azurewebsites.net/index.html?WT.mc_id=iotcurriculum-github-jabenn).

