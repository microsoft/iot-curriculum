# Clean up

In the [previous step](./ControlTheLEDThreshold.md) you wrote an Azure Function to configure the threshold for the LED colour using a Device Twin. In this step you will clean up the resources you have used.

## Delete the resource group

All the Azure resources you created were provisioned in the same resource group, called `temperaturesensor`. By having these resources in the same resource group, you can manage them together, including deleting them by deleting the entire resource group in one go.

Each resource you use reduces the number of free services you can provision or cost the credit from the free account, or can cost money from a pay as you go or enterprise account. Therefore you should delete any resources as soon as you are finished with them.

* Open the [Azure Portal](https://portal.azure.com/?WT.mc_id=academic-7372-jabenn).
* Search for the `temperaturesensor` Resource Group.
* From the *Overview* page, click **Delete Resource Group**.
* Enter the resource group name when prompted, and click **Delete**
* The resource group will be deleted and you will be notified when this is complete

<hr>

In this step you deleted the resources created by this workshop.